// /*loads jquery default slider*/
// $(function() {  
//     $( "#slider" ).slider({
//     	range: "min",  
    
//     value: 23, });  
// });  
// defining the large music slider
$(function() {  
    $( "#musicSlider" ).slider({
    	 range: "min",  
         value: 0 ,
});  
    });  



$(function() {

    var slider = $('#slider');
       


    slider.slider({
        range: "min",
        min: 1,
        value: 75,
    });

    // smooth animation of the handle
      slider.slider({
                animate: true
            });
      // mute and full volume on clicking the volume icon


    // $("#slider").find("div").click(function() {
    //                var value = slider.slider('value');
    //             volume = $('#volumeicons i');

           

    //         if(value <= 5) { 
    //             volume.removeClass().addClass( "icon-volume-off" );
    //         } 
        
    //         else if (value <= 65) {
    //             volume.removeClass().addClass( "icon-volume-down" );
    //         } 
    //         else {
    //             volume.removeClass().addClass( "icon-volume-up" );
    //         };
    // });


    $( "#volumeicons" ).click(function() {
           volume = $('#volumeicons i');

     
    });


});

