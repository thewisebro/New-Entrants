

// $(window).resize(function() {
// 	var width = document.getElementById("container").offsetWidth;
// 		var x,y;
//     for(x = 170 ; x <= 240 ; x=x+5){
//     	var n = Math.floor(width/x) ;
//     	y = (width%x)/(n);
//     	if(y>10 && y<15){
//     		break;
//     	}
//     	y = 20;
//     }
//    $(".item").css( "width", x );
//    $(".item_wrapper").css("padding-right", Math.floor(y));
//    console.log(width);
//    console.log(x);
//    console.log(y);

 
// });
 



//container item_wrapper item 
  function resizeit(divwidth,itemwrapper,itemimage) {
    // width of the div .. "divwidth"   artists_items
    // class of the complete item .. "itemwrapper"  item_wrapperAlb
    //class of the item image .. "itemimage"   itemAlb
  // get width of the container
  var width= $("#"+divwidth+"").width()-5;
 // var width = document.getElementById(""+divwidth+"").offsetWidth;
  // x=width of box to be resized , y=distance b/n 2 boxes
    var x,y,n=0;
    var i=0;
    $("."+itemwrapper+"").css("margin-right", Math.floor(0));
    $("."+itemwrapper+"").css("margin-left", Math.floor(0));

    // setting the lower limit to 170 and going upto 240 .. and in each loop checking 
    // if the y satisfies our condition for that particular width of the box.
    for(x = 140 ; x <= 250 ; x=x+5){
      n = Math.floor(width/x);
      // n is the max no of boxes that can be fit into the container length when
      // width of the box is x
      // finding the value of y

      ypre = (width%x)/(n+1);
      y = Math.floor(ypre*10)/10;
      if(y>20 && y<30){
        break;
      }
     // y = 20;
  //     y = 20;
      // console.log(y);
      //  console.log(x);
     //    console.log("--------------");
     // console.log(width+" : "+x+" : "+n)
    }
   // console.log(y);
 //   console.log(x);
   //  console.log(width+" : "+x+" : "+n);
    $("."+itemwrapper+"").css("margin-right", y);
    $("."+itemwrapper+"").css("margin-top", y);
console.log(n+"final");
   var k =1;
   var noOfItems = $("."+itemwrapper+"").length;
   for (i=0; i<=noOfItems-1 ; i=i+n){
    // var lol = $($("."+itemwrapper+"")[i]).attr('id');
    // console.log(lol);
      
       $($("."+itemwrapper+"")[i]).css("margin-left", y);

   }

   //console.log(x);
  // console.log(y);
    $("."+itemimage+"").css( "width", x );
     $("."+itemimage+"").css( "height", x );
     $(".artist_data").css("width",x);
}







// $(window).resize(function() {

//       //check if the link is selected and is either trending or albums


//   // get width of the container
//   var width = document.getElementById("artists_items").offsetWidth;
//   // x=width of box to be resized , y=distance b/n 2 boxes
//     var x,y,n=0;
//     var i=0;
//     $(".item_wrapperAlb").css("padding-right", Math.floor(0));
//     $(".item_wrapperAlb").css("padding-left", Math.floor(0));

//     // setting the lower limit to 170 and going upto 240 .. and in each loop checking 
//     // if the y satisfies our condition for that particular width of the box.
//     for(x = 170 ; x <= 350 ; x=x+5){
//       n = Math.floor(width/x) ;
//       // n is the max no of boxes that can be fit into the container length when
//       // width of the box is x
//       // finding the value of y

//       y = (width%x)/(n+1);
//       if(y>10 && y<15){
//         break;
//       }
//       y = 20;
//       // setting default value of y = 20 in case the loop ends and no perfect 
//       // setting is found

//     }
  
//    // $(".item_wrapper").css("padding-right", Math.floor(y));
//    console.log(width);
//    console.log(x);
//    console.log(y);
//    // $(".itemAlb").css( "width", x );
//     $(".item_wrapperAlb").css("padding-right", y);
//     // $($(".item_wrapperAlb")[0]).css("padding-left", Math.floor(y));
//    var k =1;
//    var noOfItems = $(".item_wrapperAlb").length;
//    for (i=0; i<=noOfItems-1 ; i=i+n){
//     // if(i==1){$($(".item_wrapperAlb")[i-1]).css("padding-left", Math.floor(y));}
//     // else{
//        $($(".item_wrapperAlb")[i]).css("padding-left", y);
//      //   if(i+n-1 <= noOfItems){
//      //   $($(".item_wrapperAlb")[i+n-1]).css("padding-right", Math.floor(y));
//      // }

//      // for(k=i-1;k<=i+n-2;k++){
//      //   $($(".item_wrapperAlb")[k]).css("padding-right", Math.floor(y));
//        // alert("after loop"+i);
//      // }
// // }

//    }

//     $(".itemAlb").css( "width", x );
   
//  // $(".itemAlb").animate({width:x}, 400, function() {
//  //    // Animation complete.
//  //  });
   
//  // $(".item_wrapperAlb").animate({paddingRight: Math.floor(y)}, 300, function() {
//  //    // Animation complete.
//  //  });

 
// });







// menu bar on left

  $( document ).ready(function() {


  //  $("#centerdata").on("click",".list_alpha ul li",function(){
   // var h = ($('#artist_banner').width()/8)*3;
    //$('#artist_banner').css("height", h);

    //  });

      // hide show
    $("#centerdata").on("click","#artist_panel_hide",function(){
    
           var $this = $(this);
            if($this.hasClass('selectedthing')){
               $this.removeClass("selectedthing");
               $("#artist_view").animate({left:'200', right:'0'},200);
              $("#artist_panel_hide").animate({left:'420', top:'145'},200);
             // $("#rightside").animate({right:'0'},200);
            }
            else{
              $this.addClass("selectedthing");
              $("#artist_view").animate({left:'0', right:'200'},200);
              $("#artist_panel_hide").animate({left:'200', top:'145'},200);
             // $("#rightside").animate({right:'220'},200);
            }

    });

    $("#centerdata").on("click","#album_panel_hide",function(){
    
           var $this = $(this);
            if($this.hasClass('selectedthing')){
               $this.removeClass("selectedthing");
               $("#oneAlbumOpened").animate({left:'220', right:'0'},200);
                $("#album_panel_hide").animate({left:'420', top:'182'},200);
               //   $("#rightside").animate({right:'0'},200);
              

            }
            else{
              $this.addClass("selectedthing");
              $("#oneAlbumOpened").animate({left:'0', right:'220'},200);
              $("#album_panel_hide").animate({left:'200', top:'182'},200);
                // $("#rightside").animate({right:'220'},200);
            }

    });
   
 
    $("#centerdata").on("click","#playlist_panel_hide",function(){
    
           var $this = $(this);
            if($this.hasClass('selectedthing')){
              $this.removeClass("selectedthing");
              $("#playlist_view").animate({left:'220', right:'0'},200);
              $("#playlist_panel_hide").animate({left:'420', top:'145'},200);
            //  $("#rightside").animate({right:'0'},200);
            }
            else{
              $this.addClass("selectedthing");
              $("#playlist_view").animate({left:'0', right:'220'},200);
              $("#playlist_panel_hide").animate({left:'200', top:'145'},200);
             // $("#rightside").animate({right:'220'},200);
            }

    });
      
   

    //delete a item from queue
    $(".trash").click(function(){
       var $this = $(this);
       var item = $this.parent();
      // item.slideUp("fast", function() {  item.fadeOut(100, function(){ $(this).remove();});});
      // item.fadeOut(300, function(){ $(this).remove();});
          item.slideUp(50, function() {
              item.fadeOut(100, function(){ $(this).remove();});
          });

            
            
    });


//song_options




    // change the color of selected link to white 
        $('#navigation').children('a').click(function(){
             $('#navigation').find('a').each(function(){
              if($(this).hasClass('selected'))
                $(this).removeClass('selected');
                
                });
             $(this).addClass('selected');
            
        });

        //   $('#navigation').children('a')
        // .mouseover(function() {
        //     var $this = $(this);
        //     if(!($this.data('clicked')){
        //        // $this.find('i').stop().animate({fontSize:'15'});
        //        $this.animate({color:'blue'},100);
        //     } 
        //     else{
        //        // $this.find('i').animate({fontSize:'15'});
        //        $this.animate({backgroundColor:'#EEE'},100);
        //     }
        // })
        // .mouseout(function() {
        //         var $this = $(this);
        //         $this.animate({backgroundColor:''},100);
        // });



    //playlist animation
    $("#playlists").click(function(){
            var $this = $(this);
            if($this.data('clicked')) {
                //alert("clicked");
                $this.find('i').removeClass().addClass("icon-heart");
                 $this.find('i').animate({marginLeft:'0'},200);
                 $this.data('clicked',false);
                // $('#playlist_view').fadeOut(50);
                 $('#playlist_view').hide();
                 
            }
            else {
                $this.data('clicked', true);
                 $this.find('i').removeClass().addClass("icon-remove");
                  $this.find('i').animate({marginLeft:'130'},200);
                  // $('#playlist_view').fadeIn(100);
                   $('#playlist_view').slideDown( "fast" );
                     
               // alert("not clicked");
            }
    });
   
// add resize class only to trending and albums
$(window).resize(function() {
//playlist images 
  var widthOfDiv = $('#playlist_view').width()/5;
       $('#playlistBanner ul li').css({width:widthOfDiv,height:widthOfDiv});
       $('#playlistBanner').css({height:widthOfDiv});
       $('#layerBanner').css({top:widthOfDiv-100+5});
        $("#playlistInfo").css({top:widthOfDiv-100+5+50});


 //resizeit('artists_items','item_wrapperAlb','itemAlb');


if($("#navigation a.selected")[0]==$("#playlists_link")[0]){
        var widthOfDiv = $('#playlist_view').width()/5;
                    $('#playlistBanner ul li').css({width:widthOfDiv,height:widthOfDiv});
                                $('#playlistBanner').css({height:widthOfDiv});
                                var tops = widthOfDiv-100;
                                $('#layerBanner').css({top:tops+5});
                                $("#playlistInfo").css({top:tops+50});

}
if($("#navigation a.selected")[0]==$("#trending_link")[0]){
resizeit('container','item_wrapper','item');
}

});


var k=10;
//playque animation
    $("#qheader").click(function(){
            
             //check if play queue is empty 
            if(!($(".qitem").length)){
            if(k==10){
                $("#qlist").append("<div>no items</div>");
                k=0;
            }
            }

            var $this = $(this);
            if($this.data('clicked')) {
               
                $this.find('i').removeClass().addClass("icon-align-justify");
                 $this.find('i').animate({marginLeft:'0'},200);
                 $this.data('clicked',false);
                // $('#playlist_view').fadeOut(50);
                 $('#qlist').hide();
                 
                 $('#play_queue').animate({marginLeft:'16'},200);
            }
            else {
                $this.data('clicked', true);
                 $this.find('i').removeClass().addClass("icon-remove");
                  $this.find('i').animate({marginLeft:'180'},200);
                  // $('#playlist_view').fadeIn(100);
                   $('#qlist').slideDown( "fast" );
                 
                  $('#play_queue').animate({marginLeft:'-6'},200);
            }
    });





  });//document.ready









