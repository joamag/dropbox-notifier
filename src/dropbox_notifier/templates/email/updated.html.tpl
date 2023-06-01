{% extends "email/layout.html.tpl" %}
{% block title %}{{ title|default(subject, True)|default("Folder updated", True) }}{% endblock %}
{% block content %}
    <h3>⚠️ The Dropbox folder {{ folder }} has just been updated ⚠️</h3>
    {% if added_entries %}
        <p>The following files have been <strong>added</strong>:</p>
        <ul>
            {% for added_entry in added_entries %}
                <li><strong>{{ added_entry.path_lower }}</strong></li>
            {% endfor %}
        </ul>
        <p>The added files have been added as attachments.</p>
    {% endif %}
    {% if removed_entries %}
        <p>The following files have been <strong>removed</strong>:</p>
        <ul>
            {% for removed_entry in removed_entries %}
                <li><strong>{{ removed_entry.path_lower }}</strong></li>
            {% endfor %}
        </ul>
    {% endif %}
{% endblock %}
