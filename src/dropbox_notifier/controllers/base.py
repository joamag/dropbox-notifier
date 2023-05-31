#!/usr/bin/python
# -*- coding: utf-8 -*-

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

    @appier.route("/scheduler", "GET")
    async def scheduler(self):
        import time

        api = self.get_api()

        previous_entries: dict[str, object] | None = None
        previous_ids: list[str] | None = None

        while True:
            self.logger.debug("Running new logger")

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
                print(f"ADDED -> {added_entries}")
                print(f"Removed ->  {removed_entries}")

            previous_ids = ids
            previous_entries = entries_m

            print(contents)
            time.sleep(30)

    @appier.route("/admin/email.json", "GET")
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
        )
        return dict(email=email)

    def get_api(self) -> dropbox.API:
        return dropbox.API(access_token=appier.conf("DROPBOX_TOKEN"))
