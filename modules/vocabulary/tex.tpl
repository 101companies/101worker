
\begin{tabular} {% block header %} {{ '{|' }}{% for col in data[0].keys() %}c{% if not loop.last %}|{% endif %}{% endfor %}{{ '|}' }} {% endblock %}
\hline
{% for col in data[0].keys() %} \textbf{ {{col}} } {% if not loop.last %}&{% endif %} {% endfor %}
\\
\hline
{% for d in data %}
    {% for k in d.keys() %}
            {{ d[k] }}{% if not loop.last %} & {% endif %}
       {% endfor %}
    \\
{% endfor %}
\hline
\end{tabular}
