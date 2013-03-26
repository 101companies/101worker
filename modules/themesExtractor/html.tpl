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
      <td>{{len(d['features'])}}</td>
      <td>{{len(d['ufeatures'])}}</td>
      <td>{{len(d['languages'])}}</td>
      <td>{{len(d['ulanguages'])}}</td>
      <td>{{len(d['technologies'])}}</td>
      <td>{{len(d['utechnologies'])}}</td>
      <td>{{len(d['concepts'])}}</td>
      <td>{{len(d['uconcepts'])}}</td>
      <td>{{d['headline']}}</td>
    </tr>
{% endfor %}
</table>

</body>

</html>

