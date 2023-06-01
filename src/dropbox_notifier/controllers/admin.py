#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

import appier
import appier_extras

from .root import RootController


class AdminController(RootController):
    @appier.route("/admin/schedule.json", "GET", json=True)
    async def scheduler(self):
        folder_path = appier.conf("NOTIFIER_FOLDER", None)
        email = self.field("email", None)
        folder_path = self.field("folder", folder_path)
        if not email:
            raise appier.OperationalError(message="No email defined")
        self.schedule(email, folder_path=folder_path)

    @appier.route("/admin/email.json", "GET", json=True)
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

    def schedule(self, email: str, folder_path: str, owner=None, sleep=30):
        owner = owner or appier.get_app()
        api = self.get_api()

        folder_meta = api.metadata_file(folder_path)
        folder_path = folder_meta["path_display"]

        previous_entries: dict[str, object] | None = None
        previous_ids: list[str] | None = None

        while True:
            try:
                self.logger.debug(f"Scanning '{folder_path}' for changes...")

                contents = api.list_folder_file(folder_path, recursive=True)
                entries_m = dict(
                    (entry["id"], entry) for entry in contents.get("entries", [])
                )
                ids = [entry["id"] for entry in contents["entries"]]
                ids.sort()

                if previous_ids and previous_entries and not ids == previous_ids:
                    added = [id for id in ids if not id in previous_ids]
                    removed = [id for id in previous_ids if not id in ids]
                    added_entries = [entries_m[id] for id in added]
                    removed_entries = [previous_entries[id] for id in removed]

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
                        subject=self.to_locale(f"Dropbox folder {folder_path} updated"),
                        attachments=added_files,
                        added_entries=added_entries,
                        removed_entries=removed_entries,
                        folder_path=folder_path,
                        prefix_size=len(folder_path),
                    )

                previous_ids = ids
                previous_entries = entries_m
            except Exception as exception:
                self.log_error(exception)

            time.sleep(sleep)
