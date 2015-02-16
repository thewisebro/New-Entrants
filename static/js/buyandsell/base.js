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


function formsearch() {
      var timer;
      alert("hi");
        $("#id_item_name").keyup(function() {
        clearTimeout(timer);
         var ms = 200; 
         var val = this.value;
         timer = setTimeout(function() { lookup(val);}, ms);
         });
        }

function lookup(val)
{
    $.ajax({
     type:"GET",    
     url:"/buyandsell/sellformsearch/",
     data:{
     'keyword':val
     },
     success:function(data){
         alert(data);
         }
         });
}

formsearch();



