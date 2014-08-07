$(document).ready(function(){


    $(" .visible_details ").click(function(e){
        //$(" .visible_details").next().css("display","none");
        $(" .visible_details").next().slideUp('slow');
        $(" .visible_details").css({ backgroundColor:"#ebebeb" , color:"#4d4d4d" });


        if(  $(this).next().css("display") == "none"  ){
            $(this).next().slideDown('slow');
            $(this).css({ backgroundColor:"#4d4d4d" , color:"#ebebeb" });
        }

        else if (  $(this).next().css("display") == "block"  ){
            $(this).next().slideUp('slow');
            $(this).css({ backgroundColor:"#ebebeb" , color:"#4d4d4d" });
        }

    });



    if($("#visible_details_item").offset())
    {
        if(  $("#visible_details_item").next().css("display") == "none"  ){
            $("#visible_details_item").next().slideDown('slow');
            $("#visible_details_item").css({ backgroundColor:"#4d4d4d" , color:"#ebebeb" });
        }


        $('html, body').animate({
            scrollTop: $('#visible_details_item').offset().top
        });
    }



    //select all the div tag with name equal to #popup
    $('div.send_email').click(function(e) {

        //Get the div tag
        var id = $(this).next();
        //Get the 'mask' div tag
        var mask = $(id).next();

        //Get the screen height and width
        var maskHeight = $(document).height();
        var maskWidth = $(window).width();

        //Set height and width to mask to fill up the whole screen
        $(mask).css({'width':maskWidth,'height':maskHeight});
        //$(mask).css({'width':'100%','height':'100%'});

        //transition effect
        $(mask).fadeIn(1000);
        $(mask).fadeTo("slow",0.8);

        //Get the window height and width
        var winH = $(window).height();
        var winW = $(window).width();

        //Set the popup window to center
        $(id).css('top',  winH/2-$(id).height()/2);
        $(id).css('left', winW/2-$(id).width()/2);

        //transition effect
        $(id).fadeIn(2000);

    });


    //if mask is clicked
    $('.mask').click(function () {
        var x = $(this).prev();
        $(x).hide();                // hiding the window
        $(this).hide();             // hiding the mask
    });







});


