#!/usr/bin/python
# -*- coding: utf-8 -*-

import typing

import appier

from dropbox import API

from dropbox_notifier.models import APIConfig


class RootController(appier.Controller):
    def ensure_api(self) -> typing.Union[str, None]:
        api_config = self.get_api_config()
        if api_config.access_token:
            return None
        api = self.get_api()
        return api.oauth_authorize()

    def get_api(self) -> API:
        api_config = self.get_api_config()
        return api_config.get_api()

    def get_api_config(self) -> APIConfig:
        api_config = APIConfig.singleton()
        api_config = typing.cast(APIConfig, api_config)
        return api_config
