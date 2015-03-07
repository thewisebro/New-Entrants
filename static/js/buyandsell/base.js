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
        $("#id_item_name").keyup(function() {
        clearTimeout(timer);
         var ms = 200; 
         var val = this.value;
         console.log(val);
        var type= window.location.href.split("/")[4];
         timer = setTimeout(function() { lookup(val,type);}, ms);
         });
        }
function lookup(val,type)
{
      search_url=bring_search_url(val);
     if(type=="sell")
     { 
       search_type="sell";
       url="/buyandsell/search/"+search_type+"/?keyword="+search_url;
     }
     else
     {
       search_type="request";
       url="/buyandsell/search/"+search_type+"/?keyword="+search_url;
     }  
    $.ajax({
     type:"GET",    
     url:url,
     success:function(data){
         alert(data[0].name);
         }
         });
}
function bring_search_url(val)
    {    var url="";
          query=val.split(" ");
          t=0;
          k=query.length;
          for(var i=0; i<k;i++)
          {
            if(query[t]=="")
              query.splice(t,1);
            else
              t++;
          }
         console.log(query+"query");
          for(var i=0; i<query.length; i++)
          { if(i!=query.length-1)
            {
            url+=query[i]+"+";
            }
            if(i==query.length-1)
            {
              url+=query[i];
            }
          }
     console.log(url);
      return url;
}
formsearch();
