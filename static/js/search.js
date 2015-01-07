$(document).ready(function() {

    $('#test').keyup(function() {
        var query;
        query = $(this).val();
        $.get('/rango/suggest_category/', {suggestion: query}, function(data){
            $('#cats').html(data);

        });
    });
});