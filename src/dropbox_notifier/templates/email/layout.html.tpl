{% extends "admin/email/layout.html.tpl" %}
{% set btitle = config.conf("TITLE", "Whistler") %}
{% set bdescription = config.conf("META_DESCRIPTION", "Whistler") %}
{% set bkeywords = config.conf("KEYWORDS", "whistler,whistleblowing") %}
{% set bauthor = config.conf("AUTHOR", "Hive Solutions Lda.") %}
{% set bwebsite = config.conf("WEBSITE", "whistler.com") %}
{% set binstagram = config.conf("INSTAGRAM", "hivesolutions") %}
{% set btwitter = config.conf("TWITTER", "hivesolutions") %}
{% set bfacebook = config.conf("FACEBOOK", "hivesolutions") %}
{% set bsemail = config.conf("SUPPORT_EMAIL", "geral@hive.pt") %}
{% set bsphone = config.conf("SUPPORT_PHONE", "+1 000 000 000") %}
{% set breviewurl = config.conf("REVIEW_URL", None) %}
{% set bhashtags = config.conf("HASHTAGS", None, cast = "list") %}
{% block background_color scoped %}#fafafa{% endblock %}
{% block content scoped %}{% endblock %}
