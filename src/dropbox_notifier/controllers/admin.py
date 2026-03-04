#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier
import appier_extras

from typing import cast

from .root import RootController


class AdminController(RootController):
    @appier.route("/admin/email", "GET", json=True)
    @appier.ensure(token="admin", context="admin")
    def email_test(self, owner=None):
        owner = owner or appier.get_app()
        email = self.field("email", None)
        if not email:
            raise appier.OperationalError(message="No email defined")
        appier_extras.admin.Base.send_email_g(
            owner,
            "email/test.html.tpl",
            receivers=[email],
            subject=self.to_locale("Dropbox Notifier test email"),
            attachments=[
                appier.FileTuple.from_data(
                    b"hello world", name="hello.txt", mime="text/plain"
                )
            ],
        )
        return dict(email=email)

    @appier.route("/admin/resend", "GET", json=True)
    @appier.ensure(token="admin", context="admin")
    def resend(self, owner=None):
        owner = owner or appier.get_app()
        owner = cast(appier.App, owner)

        since = self.field("since", None)
        if not since:
            raise appier.OperationalError(message="No since timestamp defined")

        email = cast(str, appier.conf("NOTIFIER_EMAIL", None))
        receivers = cast(list, appier.conf("NOTIFIER_RECEIVERS", [], cast=list))
        cc = cast(list, appier.conf("NOTIFIER_CC", [], cast=list))
        bcc = cast(list, appier.conf("NOTIFIER_BCC", [], cast=list))
        reply_to = cast(list, appier.conf("NOTIFIER_REPLY_TO", [], cast=list))
        folder_path = cast(str, appier.conf("NOTIFIER_FOLDER", None))

        if not folder_path:
            raise appier.OperationalError(message="No notifier folder defined")
        if not email and not receivers:
            raise appier.OperationalError(message="No email or receivers defined")

        (
            added_entries,
            added_files,
            folder_path,
            shared_base,
            shared_query,
            prefix_size,
        ) = self._resend(folder_path, since=since)

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
            removed_entries=[],
            folder_path=folder_path,
            folder_url=shared_base,
            folder_query=shared_query,
            prefix_size=prefix_size,
        )

        return dict(since=since, resent=len(added_files))

    def _resend(self, folder_path, since=None):
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
            # controls will allow deep shared folder
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
        entries = contents.get("entries", [])

        # filters the entries to only include files that have been
        # modified after the provided since timestamp value
        added_entries = [
            entry
            for entry in entries
            if entry.get(".tag") == "file"
            and entry.get("server_modified", "") >= since
            and entry.get("path_display", None)
        ]

        added_files = []

        for added_entry in added_entries:
            contents, result = api.download_file(added_entry["id"])
            content_type = appier.FileTuple.guess(result["name"])
            file_tuple = appier.FileTuple.from_data(
                contents,
                name=added_entry["path_display"][prefix_size:],
                mime=content_type or "application/octet-stream",
            )
            added_files.append(file_tuple)

        return (
            added_entries,
            added_files,
            folder_path,
            shared_base,
            shared_query,
            prefix_size,
        )
