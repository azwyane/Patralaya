{% block jquery %}
    $("button#follow").click(function(){
        $.post(
            "{% url 'user_follow' %}",
            {
                username:"{{user.user.username}}",
                action:"follow",
                csrfmiddlewaretoken: "{{csrf_token}}"
            }
            

        )
    })
{% endblock %}