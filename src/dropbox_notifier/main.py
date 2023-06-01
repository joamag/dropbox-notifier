#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier
import appier_extras


class DropboxNotifierApp(appier.WebApp):
    def __init__(self, *args, **kwargs):
        appier.WebApp.__init__(
            self,
            name="dropbox-notifier",
            parts=(appier_extras.AdminPart,),
            *args,
            **kwargs
        )

    def _version(self) -> str:
        return "0.1.0"

    def _description(self) -> str:
        return "Dropbox Notifier"

    def _observations(self) -> str:
        return "Simple Dropbox Notifier"


if __name__ == "__main__":
    app = DropboxNotifierApp()
    app.serve()
else:
    __path__ = []
