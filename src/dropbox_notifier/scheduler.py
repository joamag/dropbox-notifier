#!/usr/bin/python
# -*- coding: utf-8 -*-

import typing

import appier
import appier_extras

import dropbox

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
            timeout=typing.cast(
                float, appier.conf("SCHEDULER_TIMEOUT", LOOP_TIMEOUT, cast=int)
            ),
            *args,
            **kwargs,
        )
        self.previous_entries: dict[str, object] | None = None
        self.previous_ids: list[str] | None = None

    def tick(self):
        appier.Scheduler.tick(self)

        email: str = typing.cast(str, appier.conf("NOTIFIER_EMAIL", None))
        folder_path: str = typing.cast(str, appier.conf("NOTIFIER_FOLDER", None))

        self.logger.debug("Start of tick operation ...")
        if email and folder_path:
            self.scan_folder(email, folder_path)
        self.logger.debug("Ended tick operation")

    def scan_folder(self, email: str, folder_path: str, owner=None):
        self.logger.debug(f"Scanning '{folder_path}' for changes...")

        owner = owner or appier.get_app()
        api = self.get_api()

        folder_meta = api.metadata_file(folder_path)
        folder_path = folder_meta["path_display"]

        contents = api.list_folder_file(folder_path, recursive=True)
        entries_m = dict((entry["id"], entry) for entry in contents.get("entries", []))
        ids = [entry["id"] for entry in contents["entries"]]
        ids.sort()

        if self.previous_ids and self.previous_entries and not ids == self.previous_ids:
            added = [id for id in ids if not id in self.previous_ids]
            removed = [id for id in self.previous_ids if not id in ids]
            added_entries = [entries_m[id] for id in added]
            removed_entries = [self.previous_entries[id] for id in removed]

            added_files = []

            for added_entry in added_entries:
                contents, result = api.download_file(added_entry["id"])
                content_type = appier.FileTuple.guess(result["name"])
                file_tuple = appier.FileTuple.from_data(
                    contents,
                    name=added_entry["path_display"],
                    mime=content_type or "application/octet-stream",
                )
                added_files.append(file_tuple)

            appier_extras.admin.Base.send_email_g(
                owner,
                "email/updated.html.tpl",
                receivers=[email],
                subject=owner.to_locale(f"Dropbox folder {folder_path} updated"),
                attachments=added_files,
                added_entries=added_entries,
                removed_entries=removed_entries,
                folder_path=folder_path,
                prefix_size=len(folder_path),
            )

        self.previous_ids = ids
        self.previous_entries = entries_m

    def get_api(self) -> dropbox.API:
        return dropbox.API(access_token=appier.conf("DROPBOX_TOKEN"))
