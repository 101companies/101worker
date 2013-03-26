
<html>

<body>

<table border="3" frame="void" cellspacing="5">
<thead>
    <tr>
      {% for d in data[0].keys() %}
      {% if data[0][d] %} <th>{{ d }}</th> {% endif %}
      {% endfor %}
    </tr>
  </thead>
{% for d in data %}
    <tr>
        {% for k in d.keys() %}
        
            {% if d[k] %}<td>{{ d[k] }}</td>{% endif %}
        {% endfor %}
    </tr>
{% endfor %}
</table>

</body>

</html>

