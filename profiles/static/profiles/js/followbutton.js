$('.follow').click(function(){
$.ajax({
    
    type: "POST",
    url: "{% url 'user_follow' username={{user.user.username}} %}",
    data: {'username': $(this).attr('name'),'action':'follow','csrfmiddlewaretoken': '{{ csrf_token }}'},
    dataType: "json",
    

});
})