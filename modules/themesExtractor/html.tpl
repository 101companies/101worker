<html>
<head>
<!--[if IE]>
   <style>
      .rotate_text
      {
         writing-mode: tb-rl;
         filter: flipH() flipV();
      }
   </style>
<![endif]-->
<!--[if !IE]><!-->
   <style>
      .rotate_text
      {
         -moz-transform:rotate(-90deg); 
         -moz-transform-origin: top left;
         -webkit-transform: rotate(-90deg);
         -webkit-transform-origin: top left;
         -o-transform: rotate(-90deg);
         -o-transform-origin:  top left;
          position:relative;
         top:20px;
      }
   </style>
<!--<![endif]-->

   <style>  
      table
      {
         border: 0.5px solid black;
         table-layout: fixed;
         border-spacing
         width: 100%; /*Table width must be set or it wont resize the cells*/
      }
      th, td 
      {
          border: 1px solid black;
          /*width: 23px;*/
      }
      .rotated_cell
      {
         height:300px;
         vertical-align:bottom
      }
      .number
      {
        width: 30px;
      }
      .impl
      {
        width: 120px;
      }
   </style>
 </head> 

<body>
<table>
  <tr>
      <th class='impl'>Impl.</th>
      <th class='rotated_cell number'><div class='rotate_text'># Features</div></th>
      <th class='rotated_cell number'><div class='rotate_text'>Unique</div></th>
      <th class='rotated_cell number'><div class='rotate_text'># Languages</div></th>
      <th class='rotated_cell number'><div class='rotate_text'>Unique</div></th>
      <th class='rotated_cell number'><div class='rotate_text'># Technologies</div></th>
      <th class='rotated_cell number'><div class='rotate_text'>Unique</div></th>
      <th class='rotated_cell number'><div class='rotate_text'># Concepts</div></th>
      <th class='rotated_cell number'><div class='rotate_text'>Unique</div></th>
      <th class='rotated_cell'><div class='rotate_text'>Headline</div></th>
  </tr>
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

