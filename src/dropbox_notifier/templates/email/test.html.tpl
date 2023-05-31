{% extends "email/layout.html.tpl" %}
{% block title %}{{ title|default(subject, True)|default("Test", True) }}{% endblock %}
{% block content %}
    This is just a test email.
{% endblock %}
