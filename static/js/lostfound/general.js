$(document).ready(function(){
    var mouse_is_inside;
    $("#search_query").focus(function(){
        $("#adv_search").css("visibility","visible");  // opening of advanced search box on the focus event of search input box...
        mouse_is_inside = true;
    });


    $("#adv_search").hover(function(){  // hover event sets position varible true, and after the end of hover event the callback function sets
        mouse_is_inside = true;          // the position variable to false so that advanced search box closes on the click event...
    },
                           function(){
                               mouse_is_inside = false;
                           });

    $(document).click(function(){
        if( mouse_is_inside == false )
        {
            $("#adv_search").css("visibility","hidden");
        }
    });

    $("#logo").hover(function(){
        $("#O2").animate({right:"262px"},1000);
        $("#O1").animate({left:"262px"},1000);
    },function(){
        $("#O2").animate({right:"0px"},1000);
        $("#O1").animate({left:"0px"},1000);
    });




});
