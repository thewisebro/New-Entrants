$(document).ready
(
    function()
    {
        //Function to write IMG goes recruiting at home page
        var jumbo = ['I','M','G',' ','g','o','e','s',' ','r','e','c','r','u','i','t','i','n','g','!'];
        var x = '';
        var i = 0;
        var y = 0;
        var intervalID = setInterval(function () {

            x = x.concat(jumbo[i]);
            //console.log(x);
            $(".jumbo-text").html(x);
            i++;

            if (++y === jumbo.length) {
                window.clearInterval(intervalID);
                $(".sub-text-to-jumbo-text").css("opacity", "1");
            }
        }, 100);

        $(".general-body-text").parent(".col-md-8:last-child").children(".division-line").hide();

        $(".update-body-text").each
        (
            function()
            {
                var $this = $(this);
                var $original_content = $this.html(); //takes all the html in the content
                var $original_text = $this.text();  //takes only the text inside the content
                //console.log(taker);
                if($original_text.length > 300)
                {
                    var trimmed_text = $original_text.substr(0,300);  //takes first 300 characters of content
                    //var original_content = taker.substr(0,taker.length);
                    //console.log(taker);
                    $this.html("<span class='trimmed-text'>" + trimmed_text + "</span>" + "<span class='trimming-dots'>" + '...'  + "</span>" + "<div class='remaining-text'>" + $original_content + "</div>");
                    $(this).siblings(".read-more-button").show(); //shows read more button if text is long
                }

                $(this).show(); // and then makes the trimmed content visible to the user
            }
        );
        //collapser($(".update-body-text"))

        $(".read-more-button").click
        (
            function()
            {
//                $(".trimming-dots").hide();
                $(this).siblings(".update-body-text").children(".trimmed-text").hide();
                $(this).siblings(".update-body-text").children(".trimming-dots").hide();
                $(this).siblings(".update-body-text").children(".remaining-text").show();
//                $(".remaining-text").show()
//                console.log("clicked");
                $(this).hide();
            }
        );

        adjustStyle($(this).width());
        $(window).resize(function() {
            adjustStyle($(this).width());
        });

/*
        for(i in jumbo)
        {
            x = x.concat(jumbo[i]);
            console.log(x);
            $(".jumbo-text").html(x);
        }
*/

    }
);


function adjustStyle(width) {
    width = parseInt(width);
    if (width < 992) {
        $("#mobile-stylesheet").attr("href", "css/mobile.css");
    }
    else {
        $("#mobile-stylesheet").attr("href", "css/index.css");
    }
}


//function to trim content at updates page

/*
function collapser(content)  //function to trim content at updates page
{
    var $this = $(this);
    var $original_content = $this.html(); //takes all the html in the content
    var $original_text = $this.text();  //takes only the text inside the content
    //console.log(taker);
    if($original_text.length > 300)
    {
        var trimmed_text = $original_text.substr(0,300);  //takes first 300 characters of content
        //var original_content = taker.substr(0,taker.length);
        //console.log(taker);
        $this.html("<span class='trimmed-text'>" + trimmed_text + "</span>" + "<span class='trimming-dots'>" + '...'  + "</span>" + "<div class='remaining-text'>" + $original_content + "</div>");
    }
}
*/

function initialize()
{
    var position = new google.maps.LatLng(29.8627129, 77.8964149);
    var mapCanvas = document.getElementById('google-map-div');
    var mapOptions =
    {
        center : position,
        zoom : 16,
        mapTypeId : google.maps.MapTypeId.ROADMAP
    };

    var map = new google.maps.Map(mapCanvas, mapOptions);

    var marker = new google.maps.Marker
    (
        {
            position:position,
            icon: "img/map-address-icon.png",
            map: map,
            draggable: false,
            animation: google.maps.Animation.DROP
        }
    );

    function toggleBounce()
    {
        if (marker.getAnimation() !== null) {
            marker.setAnimation(null);
        } else {
            marker.setAnimation(google.maps.Animation.BOUNCE);
        }
    }

    marker.addListener('click', toggleBounce);
}
