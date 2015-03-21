//watch("ELECTRONICS");
var opened_dialog="";
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
function create_div()
{
  $("<div id = \"insert\">").insertAfter("#id_item_name");
  $("<div id = \"insert_main\">").insertAfter("#search_main");
  console.log("yes");

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

     if(search_url=="" && type!="main")
     { 
       $("#insert").html("");
       return;
     }

     if(search_url=="" && type=="main")
     { 
       $("#insert_main").html("");
       return;
     } 

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
               html+="<li onclick=\"request_details("+data[i].id+")\">"+data[i].name+"</li>";
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
             html="";
             var html="<ul>"; 
             for(var i=0;i<data['main_cat'].length;i++)
             {
               html+="<a href=\"/buyandsell/buy/"+data['main_cat'][i].main_category+"\">"+data['main_cat'][i].main_category+"</a><br>";
              }
             html+="</ul>";
             html+="<ul>";
             for(var i=0;i<data['sub_cat'].length;i++)
             {
                 html+="<a href=\"/buyandsell/buy/"+data['sub_cat'][i].main_category+"/"+data['sub_cat'][i].code+"\">"+data['sub_cat'][i].name+"</a><br>";
              }
             html+="</ul>";
              html+="<ul>";
             for(var i=0;i<data['requests'].length;i++)
             {
                 html+="<li onclick=\"request_details("+data['requests'][i].id+")\">"+data['requests'][i].name+"</li>";
              }
             html+="</ul>";
             html+="<div id=\"see_all_req\">See all requests</div>";
               html+="<ul>";
             for(var i=0;i<data['sell_items'].length;i++)
             {
                 html+="<li onclick=\"sell_details("+data['sell_items'][i].id+")\">"+data['sell_items'][i].name+"</li>";
              }
             html+="</ul>";
             html+="<div id=\"see_all_sell\">See all sale items</div>";
             console.log(html);
          $("#insert_main").html(html); 
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
               html+="<li onclick=\"sell_details("+data[i].id+")\">"+data[i].name+"</li>";
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
function search_form()
 {    console.log("yo");
     var form=$("#search_form");
     console.log(form.attr("action"));

     $("body").on("click","#see_all_req",
         function(){
         form.attr("action","/buyandsell/see_all/requests/");
         form.submit();
         });

     $("body").on("click","#see_all_sell",
         function(){
         form.attr("action","/buyandsell/see_all/sell/");
         form.submit();
         } );
}
function trash(type,id)
{
     if(type=="request")
     {
       type="request";
       trash_item(type,id);
     }
     else if (type=="sell")
     {
      type="sell";
      trash_item(type,id);
     }
}
function trash_item(type,id)
{

  		  $.ajax({
    		  url : "/buyandsell/trash/"+type+"/"+id+"/",
    		  success: function (data)
    		  {
                $("#"+type+id).remove(); 
          }
          });
}
 function show_contact()
{
  $("#show_contact").change(
      function(){
     if($(this).prop("checked")==true)
     {
        $.ajax({
    		  url : "/buyandsell/show_contact/yes/",
    		  success: function (data)
    		  {
               console.log("ho gaya");

          }
              });
     }
        else
     {
          $.ajax({
    		  url : "/buyandsell/show_contact/no/",
    		  success: function (data)
    		  {
               console.log("ho gaya firse")
          }
               });
     }
      });
}

show_contact();   
//trash("sell",6);
search_form();
search();
create_div();

function sell_form(){
 if(opened_dialog !=""){
  close_dialog(opened_dialog);
  }
 console.log("kanav");
 dialog_iframe({
    name:'sell_form_dialog',
    title:'SellForm',
    width:600,
    height:360,
    src:'/buyandsell/sell/',
    close:function(){opened_dialog=""}
  });
 opened_dialog='sell_form_dialog';
}

function request_form(){
  if(opened_dialog !=""){
  close_dialog(opened_dialog);
  }
 dialog_iframe({
    name:'request_form_dialog',
    title:'RequestForm',
    width:600,
    height:360,
    src:'/buyandsell/requestitem/',
    close:function(){opened_dialog=""}
  });
 opened_dialog='request_form_dialog';
}

function sell_details(pk){
 if(opened_dialog !=""){
  close_dialog(opened_dialog);
  }
 dialog_iframe({
    name:'sell_detail_dialog',
    title:'SellItemDetails',
    width:600,
    height:360,
    src:'/buyandsell/sell_details/'+pk+'/',
    close:function(){opened_dialog=""}
  });
opened_dialog='sell_detail_dialog';
}

function request_details(pk){
 if(opened_dialog !=""){
  close_dialog(opened_dialog);
  }
 dialog_iframe({
    name:'request_detail_dialog',
    title:'RequestItemDetails',
    width:600,
    height:360,
    src:'/buyandsell/request_details/'+pk+'/',
    close:function(){opened_dialog=""}
  });
 opened_dialog='request_detail_dialog';
}

function edit_sell(pk){
 if(opened_dialog !=""){
  close_dialog(opened_dialog);
  }
 dialog_iframe({
    name:'edit_sell_dialog',
    title:'EditSellItem',
    width:600,
    height:360,
    src:'/buyandsell/edit/sell/'+pk+'/',
    close:function(){opened_dialog=""}
  });
  opened_dialog='edit_sell_dialog';
}

function edit_request(pk){
 if(opened_dialog !=""){
  close_dialog(opened_dialog);
  }
 dialog_iframe({
    name:'edit_request_dialog',
    title:'EditRequestItem',
    width:600,
    height:360,
    src:'/buyandsell/edit/request/'+pk+'/',
    close:function(){opened_dialog=""}
  });
 opened_dialog='edit_request_dialog';
}
