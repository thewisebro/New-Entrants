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
function create_div(){
  $("<div id = \"insert\">").insertAfter("#id_item_name");
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
function search() {
      var timer;
        $("#id_item_name").keyup(function() {
        clearTimeout(timer);
         var ms = 200; 
         var val = this.value;
         console.log(val);
        var type= window.location.href.split("/")[4];
         timer = setTimeout(function() { lookup(val,type);}, ms);
         });
        $("#search_main").keyup(function() {
        clearTimeout(timer);
         var ms = 200; 
         var val = this.value;
         console.log(val);
        var type= "main";
         timer = setTimeout(function() { lookup(val,type);}, ms);
         });
        }
function lookup(val,type)
{
     search_url=bring_search_url(val);

     if(search_url=="")
       return;

     if(type=="sell")
     { 
       $.ajax({
       type:"GET",    
       url:"/buyandsell/search/sell/?keyword="+search_url,
       success:function(data){
             html="";
             var html="<ul>"; 
             for(var i=0;i<data.length;i++)
             {
               html+="<li>"+data[i].name+"</li>";
              }
             html+="</ul>";
             console.log(html);
          $("#insert").html(html); 
          }
            });
            
     }
     else if(type=="main")
     {
         $.ajax({
         type:"GET",    
         url:"/buyandsell/search/main/?keyword="+search_url,
         success:function(data){

         }
            });
             
     }

     else
     {
       $.ajax({
       type:"GET",    
       url:"/buyandsell/search/request/?keyword="+search_url,
       success:function(data){
             html="";
             var html="<ul>"; 
             for(var i=0;i<data.length;i++)
             {
               html+="<li>"+data[i].name+"</li>";
              }
             html+="</ul>";
             console.log(html);
          $("#insert").html(html); 
       }
            });

           }  
    
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
search();
create_div();
