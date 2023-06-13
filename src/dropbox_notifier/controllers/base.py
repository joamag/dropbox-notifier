#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .root import RootController


class BaseController(RootController):
    @appier.route("/", "GET")
    def index(self):
        return self.me()

    @appier.route("/me", "GET")
    def me(self):
        url = self.ensure_api()
        if url:
            return self.redirect(url)
        api = self.get_api()
        account = api.self_user()
        return account

    @appier.route("/files/insert/<str:message>", "GET")
    def file_insert(self, message):
        url = self.ensure_api()
        if url:
            return self.redirect(url)
        api = self.get_api()
        path = self.field("path", "/hello")
        message = appier.legacy.bytes(message, encoding="utf-8", force=True)
        contents = api.session_start_file()
        session_id = contents["session_id"]
        contents = api.session_finish_file(session_id, data=message, path=path)
        return contents

    @appier.route("/folders/list", "GET")
    def folder_list(self):
        url = self.ensure_api()
        if url:
            return self.redirect(url)
        api = self.get_api()
        path = self.field("path", "")
        recursive = self.field("recursive", False, cast=bool)
        contents = api.list_folder_file(path, recursive=recursive)
        return contents
