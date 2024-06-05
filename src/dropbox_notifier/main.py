#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier
import appier_extras

from dropbox_notifier import scheduler


class DropboxNotifierApp(appier.WebApp):
    def __init__(self, *args, **kwargs):
        appier.WebApp.__init__(
            self,
            name="dropbox-notifier",
            parts=(appier_extras.AdminPart,),
            *args,
            **kwargs
        )
        self.scheduler = scheduler.Scheduler(self)

    def start(self):
        appier.WebApp.start(self)
        scheduler_ = appier.conf("SCHEDULER", True, cast=bool)
        if scheduler_:
            self.scheduler.start()

    def _version(self) -> str:
        return "0.2.9"

    def _description(self) -> str:
        return "Dropbox Notifier"

    def _observations(self) -> str:
        return "Simple Dropbox Notifier"


if __name__ == "__main__":
    app = DropboxNotifierApp()
    app.serve()
else:
    __path__: list[str] = []
