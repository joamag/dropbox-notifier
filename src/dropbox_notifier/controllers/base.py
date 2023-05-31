#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

import appier
import appier_extras

import dropbox


class BaseController(appier.Controller):
    @appier.route("/", "GET")
    @appier.route("/me", "GET")
    def me(self):
        api = self.get_api()
        account = api.self_user()
        return account

    @appier.route("/files/insert/<str:message>", "GET")
    def file_insert(self, message):
        api = self.get_api()
        path = self.field("path", "/hello")
        message = appier.legacy.bytes(message, encoding="utf-8", force=True)
        contents = api.session_start_file()
        session_id = contents["session_id"]
        contents = api.session_finish_file(session_id, data=message, path=path)
        return contents

    @appier.route("/folders/list", "GET")
    def folder_list(self):
        api = self.get_api()
        path = self.field("path", "")
        recursive = self.field("recursive", False, cast=bool)
        contents = api.list_folder_file(path, recursive=recursive)
        return contents

    @appier.route("/webhook", "GET")
    async def webhook_challenge(self):
        challenge = self.field("challenge")
        self.request.set_header("Content-Type", "text/plain")
        self.request.set_header("X-Content-Type-Options", "nosniff")
        return challenge

    @appier.route("/webhook", "POST")
    async def webhook_data(self):
        print(self.request.get_data())

    @appier.route("/admin/schedule.json", "GET", json=True)
    async def scheduler(self):
        email = self.field("email", None)
        if not email:
            raise appier.OperationalError(message="No email defined")
        self.schedule(email)

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

    def schedule(self, email, owner=None, sleep=30):
        owner = owner or appier.get_app()

        api = self.get_api()

        previous_entries: dict[str, object] | None = None
        previous_ids: list[str] | None = None

        while True:
            self.logger.debug("Running new logger cycle")

            contents = api.list_folder_file("id:CtYjakof0XIAAAAAAAPyEg", recursive=True)
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
                        name=added_entry["path_lower"],
                        mime=content_type or "application/octet-stream",
                    )
                    added_files.append(file_tuple)

                appier_extras.admin.Base.send_email_g(
                    owner,
                    "email/updated.html.tpl",
                    receivers=[email],
                    subject=self.to_locale("Folder updated"),
                    attachments=added_files,
                    added_entries=added_entries,
                    removed_entries=removed_entries,
                )

            previous_ids = ids
            previous_entries = entries_m

            time.sleep(sleep)

    def get_api(self) -> dropbox.API:
        return dropbox.API(access_token=appier.conf("DROPBOX_TOKEN"))
