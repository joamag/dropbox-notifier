<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename = 'css/layout.css') }}" />
</head>
<body class="order-checker">
    <table>
        <thead>
            <tr>
                <th>Order</th>
                <th>Customer</th>
                <th>Street</th>
                <th>Zip Code</th>
                <th>City</th>
                <th>Product</th>
                <th>Quantity</th>
                <th>Verify</th>
            </tr>
        </thead>
        <tbody>
            {% for order in orders %}
                {% for line in order.s_line_items %}
                    <tr>
                        <td class="highlight">{{ order.s_name }}</td>
                        <td>{{ order.s_shipping_name }}</td>
                        <td>{{ order.s_shipping_street }}</td>
                        <td>{{ order.s_shipping_zip }}</td>
                        <td>{{ order.s_shipping_city }} ({{ order.s_shipping_country_code }})</td>
                        <td class="highlight">{{ line.name }}</td>
                        <td>{{ line.quantity }}x</td>
                        <td>▢</td>
                    </tr>
                {% endfor %}
                <tr class="simple">
                    <td>&nbsp;</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
    <div class="footer">Document generated on the {{ date_time(time.time(), format = "%d %b %Y %H:%M") }} (UTC)</div>
</body>
</html>
