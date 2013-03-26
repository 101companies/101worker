
<html>

<body>

<table cellspacing='0px'>
  <tr>
      <th style="border: 0.2px solid black;">Name</th>
      <th style="border: 0.2px solid black;">Headline</th>
  </tr>
{% for d in data %}
    <tr>
      <td style="border: 0.2px solid black;">{{d['name']}}</td>
      <td style="border: 0.2px solid black;">{{d['headline']}}</td>
    </tr>
{% endfor %}
</table>

</body>

</html>

