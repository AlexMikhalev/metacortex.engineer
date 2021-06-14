Using forloop counter in django pagination
##########################################
:date: 2010-03-25 23:40
:author: Alex
:tags: Uncategorized

In order to use forloop.counter with pagination use:

{% for object in object\_list %}

{{ page\_obj.start\_index\|add:forloop.counter0 }}

{% endfor %}
