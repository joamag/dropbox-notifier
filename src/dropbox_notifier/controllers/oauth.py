#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .root import RootController


class OauthController(RootController):
    @appier.route("/oauth", "GET", json=True)
    async def oauth(self):
        code = self.field("code")
        error = self.field("error")
        appier.verify(
            not error,
            message="Invalid OAuth response (%s)" % error,
            exception=appier.OperationalError,
        )
        api_config = self.get_api_config()
        api = api_config.get_api()
        api_config.access_token = api.oauth_access(code)
        api_config.refresh_token = api.refresh_token
        api_config.save()
        return self.redirect(self.url_for("base.index"))

    @appier.route("/oauth/logout", "GET", json=True)
    async def logout(self):
        api_config = self.get_api_config()
        api_config.access_token = None
        api_config.refresh_token = None
        api_config.save()
        return self.redirect(self.url_for("base.index"))
