
<html>

<body>

<table cellspacing='0px'>
  <tr>
      <th>Name</th>
      <th>Headline</th>
  </tr>
{% for d in data %}
    <tr>
      <td>{{d['name']}}</td>
      <td>{{d['headline']}}</td>
    </tr>
{% endfor %}
</table>

</body>

</html>

