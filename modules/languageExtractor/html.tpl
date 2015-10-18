
<html>

<body>

<table border="3" frame="void" cellspacing="5">
<thead>
    <tr>
      {% if data|length > 0 %}
      {% for d in data[0].keys() %}
      <th>{{ d }}</th>
      {% endfor %}
      {% endif %}
    </tr>
  </thead>
{% for d in data %}
    <tr>
        {% for k in d.keys() %}
        
            {% if d[k] %}<td>{{ d[k]|render }}</td>{% endif %}
        {% endfor %}
    </tr>
{% endfor %}
</table>

</body>

</html>

