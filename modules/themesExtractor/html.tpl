<html>
<body>

<table border="1">
<thead>
    <tr>
      <td>Impl.</td>
      <td># Features</td>
      <td>Unique</td>
      <td># Languages</td>
      <td>Unique</td>
      <td># Technologies</td>
      <td>Unique</td>
      <td># Concepts</td>
      <td>Unique</td>
      <td>Headline</td>
    </tr>
  </thead>
{% for d in data %}
    <tr>
      <td>{{d['name']}}</td>
      <td>{{d['features']|length}}</td>
      <td>{{d['ufeatures']|length}}</td>
      <td>{{d['languages']|length}}</td>
      <td>{{d['ulanguages']|length}}</td>
      <td>{{d['technologies']|length}}</td>
      <td>{{d['utechnologies']|length}}</td>
      <td>{{d['concepts']|length}}</td>
      <td>{{d['uconcepts']|length}}</td>
      <td>{{d['headline']}}</td>
    </tr>
{% endfor %}
</table>

</body>

</html>

