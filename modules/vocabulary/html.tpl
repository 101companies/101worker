
<html>

<body>

<table border="3" frame="void" cellspacing="5">
<thead>
    <tr>
      {% for d in data[0].keys()|reverse %}
      <th>{{ d }}</th>
      {% endfor %}
    </tr>
  </thead>
{% for d in data %}
    <tr>
        {% for k in d.keys()|reverse %}
        <td>
            {{ d[k] }}
        </td>
        {% endfor %}
    </tr>
{% endfor %}
</table>

</body>

</html>

