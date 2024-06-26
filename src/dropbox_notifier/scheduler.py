#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier
import appier_extras

from typing import Any, Dict, Union, cast
from dropbox import API

LOOP_TIMEOUT = 30.0
""" The time value to be used to sleep the main sequence
loop between ticks, this value should not be too small
to spend many resources or to high to create a long set
of time between external interactions """


class Scheduler(appier.Scheduler):
    def __init__(self, owner, *args, **kwargs):
        appier.Scheduler.__init__(
            self,
            owner,
            timeout=cast(
                float, appier.conf("SCHEDULER_TIMEOUT", LOOP_TIMEOUT, cast=int)
            ),
            *args,
            **kwargs,
        )
        self.previous_entries: Union[dict[str, Dict[str, Any]], None] = None
        self.previous_ids: Union[list[str], None] = None

    def tick(self):
        appier.Scheduler.tick(self)

        email: str = cast(str, appier.conf("NOTIFIER_EMAIL", None))
        receivers: list = cast(list, appier.conf("NOTIFIER_RECEIVERS", [], cast=list))
        cc: list = cast(list, appier.conf("NOTIFIER_CC", [], cast=list))
        bcc: list = cast(list, appier.conf("NOTIFIER_BCC", [], cast=list))
        reply_to: list = cast(list, appier.conf("NOTIFIER_REPLY_TO", [], cast=list))
        folder_path: str = cast(str, appier.conf("NOTIFIER_FOLDER", None))

        self.logger.debug("Start of tick operation ...")
        if (email or receivers) and folder_path:
            self.scan_folder(
                email,
                folder_path,
                receivers=receivers,
                cc=cc,
                bcc=bcc,
                reply_to=reply_to,
            )
        self.logger.debug("Ended tick operation")

    def scan_folder(
        self,
        email: str,
        folder_path: str,
        receivers=[],
        cc=[],
        bcc=[],
        reply_to=[],
        owner=None,
    ):
        self.logger.debug(f"Scanning '{folder_path}' for changes...")

        owner = owner or appier.get_app()
        owner = cast(appier.App, owner)
        api = self.get_api()

        folder_meta = api.metadata_file(folder_path)
        folder_path = folder_meta["path_display"]
        prefix_size = len(folder_path)

        share = api.list_shared_links(folder_path)
        share_links = share.get("links", [])

        # in case valid share links exist then we should re-use the
        # best of them to create the appropriate links
        if share_links:
            shared = share_links[0]

            # loops trying to find the best possible share link
            # for the folder, keeping in mind that using extended sharing
            # controls will allows deep shared folder
            for share_link in share_links:
                link_permissions = share_link.get("link_permissions", {})
                if not link_permissions.get("can_use_extended_sharing_controls", False):
                    continue
                shared = share_link

        # creates a shared link to the folder so that it can be used
        # for the URL creation in no shared link already exists
        else:
            shared = api.create_shared_link(folder_path)

        shared_url = appier.legacy.urlparse(shared["url"])
        shared_base = f"{shared_url.scheme}://{shared_url.netloc}{shared_url.path}"
        shared_query = shared_url.query

        contents = api.list_folder_file(folder_path, recursive=True)
        entries_m = cast(
            dict[str, Dict[str, Any]],
            dict((entry["id"], entry) for entry in contents.get("entries", [])),
        )
        ids = cast(list[str], [entry["id"] for entry in contents["entries"]])
        ids.sort()

        if self.previous_ids and self.previous_entries and not ids == self.previous_ids:
            added = [id for id in ids if not id in self.previous_ids]
            removed = [id for id in self.previous_ids if not id in ids]
            added_entries = [entries_m[id] for id in added]
            removed_entries = [self.previous_entries[id] for id in removed]

            # filters out the entries that do not have a valid display path
            # this prevents "ghost" entries from being sent in the email,
            # actin as a safety measure for the email sending operation
            added_entries = [
                entry for entry in added_entries if entry.get("path_display", None)
            ]
            removed_entries = [
                entry for entry in removed_entries if entry.get("path_display", None)
            ]

            added_files = []

            for added_entry in added_entries:
                tag = added_entry.get(".tag", "file")
                if not tag == "file":
                    continue

                contents, result = api.download_file(added_entry["id"])
                content_type = appier.FileTuple.guess(result["name"])
                file_tuple = appier.FileTuple.from_data(
                    contents,
                    name=added_entry["path_display"][prefix_size:],
                    mime=content_type or "application/octet-stream",
                )
                added_files.append(file_tuple)

            appier_extras.admin.Base.send_email_g(
                owner,
                "email/updated.html.tpl",
                receivers=receivers if receivers else [email],
                cc=cc,
                bcc=bcc,
                reply_to=reply_to,
                subject=owner.to_locale(f"Dropbox folder {folder_path} updated"),
                attachments=added_files,
                added_entries=added_entries,
                removed_entries=removed_entries,
                folder_path=folder_path,
                folder_url=shared_base,
                folder_query=shared_query,
                prefix_size=prefix_size,
            )

        self.previous_ids = ids
        self.previous_entries = entries_m

    def get_api(self) -> API:
        from dropbox_notifier import APIConfig

        api_config = cast(APIConfig, APIConfig.singleton())
        return api_config.get_api()
