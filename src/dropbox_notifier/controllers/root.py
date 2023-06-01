#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

import dropbox


class RootController(appier.Controller):
    def get_api(self) -> dropbox.API:
        return dropbox.API(access_token=appier.conf("DROPBOX_TOKEN"))
