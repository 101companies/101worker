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
      <td>{{d['features']|len}}</td>
      <td>{{d['ufeatures']|len}}</td>
      <td>{{d['languages']|len}}</td>
      <td>{{d['ulanguages']|len}}</td>
      <td>{{d['technologies']|len}}</td>
      <td>{{d['utechnologies']|len}}</td>
      <td>{{d['concepts']|len}}</td>
      <td>{{d['uconcepts']|len}}</td>
      <td>{{d['headline']}}</td>
    </tr>
{% endfor %}
</table>

</body>

</html>

