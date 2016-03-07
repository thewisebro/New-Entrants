// jQuery from here
  $(document).ready(function(){
    //$('[for=id_sub_category]').css("display","none" );
    //$("div#subcategory").css("display", "none" );

    $("select#id_category").click(function (){
      //$(this).hide();i
      var category = $(this).val();
      var url = "/buysell/ajax-request/" + category +"/";
      $.get(url, function(data){
        // function goes here
        //if( 
         $("select#id_sub_category").html(data);
        });
      $('[for=id_sub_category]').css("display","inline" );
      $("div#subcategory").css("display", "inline");    
      if(category == "")
      {
        $('[for=id_sub_category]').css("display","none" );
        $("select#id_sub_category").css("display", "none" );
      }
      });
      var itemPic = $('#itemPic').html();
      var itemid = $('#itemid').html();
      var mediaurl = '/media/';
      });
