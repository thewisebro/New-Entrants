//watch("ELECTRONICS");

function watch(main_category,category)
{
   if (typeof category != "undefined")
   {
     url="/buyandsell/watch/"+main_category+"/"+category+"/";
     watch_cat(url);
   }
   else
   {
     url="/buyandsell/watch/"+main_category+"/";
     watch_cat(url);
   }
}

function watch_cat(url)
{
  		  $.ajax({
    		  url : url,
    		  success: function (data)
    		  {
      		alert("done"+data['success']);	  
          }
          });
}
