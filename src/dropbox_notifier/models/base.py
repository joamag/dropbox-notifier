#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier
import appier_extras

import dropbox


class DropboxNotifierBase(appier_extras.admin.Base):
    @classmethod
    def is_abstract(cls):
        return True

    @property
    def dropbox_api(self):
        return dropbox.API(access_token=appier.conf("DROPBOX_TOKEN"))
