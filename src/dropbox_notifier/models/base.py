#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier_extras


class DropboxNotifierBase(appier_extras.admin.Base):
    @classmethod
    def is_abstract(cls) -> bool:
        return True
