#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier
import appier_extras

from .root import RootController


class AdminController(RootController):
    @appier.route("/admin/email.json", "GET", json=True)
    @appier.ensure(token="admin", context="admin")
    async def email_test(self, owner=None):
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
