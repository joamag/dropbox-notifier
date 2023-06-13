#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

import dropbox

from .base import DropboxNotifierBase


class APIConfig(DropboxNotifierBase):
    access_token = appier.field(index=True)

    refresh_token = appier.field(index=True)

    def get_api(self):
        client_id = appier.conf("DROPBOX_ID")
        client_secret = appier.conf("DROPBOX_SECRET")
        appier.verify(client_id, message="No Dropbox Client ID set")
        appier.verify(client_secret, message="No Dropbox Client Secret set")
        redirect_url = appier.get_app().url_for("oauth.oauth", absolute=True)
        return dropbox.API(
            client_id=client_id,
            client_secret=client_secret,
            redirect_url=redirect_url,
            access_token=appier.conf("DROPBOX_TOKEN") or self.access_token,
            refresh_token=appier.conf("DROPBOX_REFRESH") or self.refresh_token,
        )
