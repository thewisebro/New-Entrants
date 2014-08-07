
$('#submit_button').click(function(){

    var type = $('#adv_search input[type=radio]:checked').val();
    var name = $('#search_query').val();

    if(type != '' && name!='')
    {
        document.location.href = '/lostfound/search/'+type+'/'+name;
    }
    else
        alert("Please fill in the details first");

});



$("#search_query").keypress(function(event) {
    if (event.which == 13) {
        event.preventDefault();
        var type = $('#adv_search input[type=radio]:checked').val();
        var name = $('#search_query').val();
        if(type != '' && name!='')
        {
            document.location.href = '/lostfound/search/'+type+'/'+name;
        }
        else
            alert("Please fill in the details first");
    }

});


