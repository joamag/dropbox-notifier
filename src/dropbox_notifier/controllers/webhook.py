#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .root import RootController


class WebhookController(RootController):
    @appier.route("/webhook", "GET")
    async def webhook_challenge(self):
        challenge = self.field("challenge")
        self.request.set_header("Content-Type", "text/plain")
        self.request.set_header("X-Content-Type-Options", "nosniff")
        return challenge

    @appier.route("/webhook", "POST")
    async def webhook_data(self):
        print(self.request.get_data())
