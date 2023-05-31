{% extends "email/layout.html.tpl" %}
{% block title %}Confirmação de pagamento {{ order.s_name }}{% endblock %}
{% block content %}
    <p>
        O pagamento para a encomenda {{ order.s_name }} acabou de ser recebido!
        Iremos processar a sua encomenda com a maior brevidade.
    </p>
    {{ h2("Estamos Sempre Consigo") }}
    <p>
        Algum problema? A nossa equipa de apoio está disponível para o ajudar.
        Envie-nos um email para {{ link("mailto:geral@oioba.com", "geral@oioba.com", False) }}.
    </p>
{% endblock %}
