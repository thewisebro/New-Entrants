//watch("ELECTRONICS");
var opened_dialog="";  //variable to keep check of the opened dialog

function watch_new(main_category,category)
{

  if($("#watch_btn").hasClass("watch-button-watching"))
  {
    if (category != "None")
    {
      url="/buyandsell/unwatch/"+main_category+"/"+category+"/";
      watch_cat(url);
    }
    else
    {
      url="/buyandsell/unwatch/"+main_category+"/";
      watch_cat(url);
    }

    $("#watch_btn").removeClass("watch-button-watching");
    $("#watch_btn").text("Watch this Category");
  }
  else
  {
    if (category != "None")
    {
      url="/buyandsell/watch/"+main_category+"/"+category+"/";
      watch_cat(url);
    }
    else
    {
      url="/buyandsell/watch/"+main_category+"/";
      watch_cat(url);
    }
    $("#watch_btn").addClass("watch-button-watching");
    $("#watch_btn").text("Watching");
  }

}

function watch_cat(url)
{
  $.ajax({
    url : url,
    success: function (data)
    {
     if(data['success'] == 'false'){
          window.location.reload();
          }

    }
  });
}

function search() {
  var timer;
 /* $("#id_item_name").keyup(function() {
    clearTimeout(timer);
    var ms = 200;
    var val = this.value;
    console.log(val);
    var type= window.location.href.split("/")[4];
    timer = setTimeout(function() { lookup(val,type);}, ms);
  });
  */
  $(".search-form").keyup(function() {
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

  /*     if(search_url=="" && type!="main")
   {
   $("#insert").html("");
   return;
   }
   */
  if(search_url=="" && type=="main")
  {
    $(".search-result-box").html("");
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
        html+="<div class = \"search-result-categories\">";

        for(var i=0;i<data['main_cat'].length;i++)
        {
          html+="<a href=\"/buyandsell/buy/"+
            data['main_cat'][i].main_category+"\">"+
            "<div class = \"searched-category\">"+
            data['main_cat'][i].main_category+
            "</div></a>";
        }


        for(var i=0;i<data['sub_cat'].length;i++)
        {
          html+="<a href=\"/buyandsell/buy/"+
            data['sub_cat'][i].main_category+"/"+data['sub_cat'][i].code+"\">"+
            "<div class = \"searched-category\">"+
            data['sub_cat'][i].name+
            "</div></a>";
        }

        if ( data['sell_items'].length )
        {

          html+="<div class = \"visible-division-line\"></div>"+
            "<div class = \"searched-items-for-sale\">"+
            "<p class=\"search-results-heading\">"+
            "<span class=\"searched-query\">"+val+"</span>&nbsp"+
            "in Items for Sale</p>";

          for(var i=0;i<data['sell_items'].length;i++)
          {
            html+="<a class=\"searched-item instant-searched-item-for-sale\" onclick=\"sell_details("+data['sell_items'][i].id + ",'" +
              data['sell_items'][i].name + "'" + ")\">"+
              '<div>'+
              '<span class="searched-item-name">'+
              data['sell_items'][i].name+
              '</span>'+
              ' <span class="searched-item-price">'+
              data['sell_items'][i].cost+
              '</span>'+
              ' <span class="rupee-logo"><img class="rupee-icon" src="' +  static_url + '/images/buyandsell/rupee-icon.png">&nbsp</span>'+
              ' </div>'+
              "</a>";

          }

          html+='</div>'+
            '<a id="see_all_sell" class="see-all-items-for-sale">See all</a>';
        }
        else
        {
          html+="<div class = \"visible-division-line\"></div>"+
            "<div class = \"searched-items-for-sale\">"+
            "<p class=\"search-results-heading\">"+
            "No such Item found.</p>"+
            "</div>";
        }

        html += "</div>" +
          "<div class = \"visible-division-line\"></div>"+
          "<div class = \"searched-items-for-sale\">";

        if ( data['requests'].length )
        {
          html+="<p class=\"search-results-heading\">"+
            "<span class=\"searched-query\">" + val +"</span>&nbsp"+
            '<span class="max-price-heading">Max Price</span>'+
            "in Requests</p>";

          for(var i=0;i<data['requests'].length;i++)
          {
            html+="<a class=\"searched-item instant-searched-request\" onclick=\"request_details("+data['requests'][i].id+",'" +
              data['requests'][i].name + "'" + ")\">" +
              '<div>'+
              '<span class="searched-item-name">'+
              data['requests'][i].name+
              '</span>'+
              ' <span class="searched-item-price">'+
              data['requests'][i].price_upper+
              '</span>'+
              ' <span class="rupee-logo"><img class="rupee-icon" src="' +  static_url + '/images/buyandsell/rupee-icon.png">&nbsp</span>'+
              ' </div>'+
              "</a>";
          }
          html+='</div>'+
            '<a id="see_all_req" class="see-all-items-for-sale">See all</a>';
        }
        else
        {

          html+="<p class=\"search-results-heading\">"+
            "No such request found.</p>"+
            "</div>";
        }


        $(".search-result-box").html(html);
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
{
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
        if(data['success'] == 'false'){
          window.location.reload();
          }
          else{
      $("#"+type+id).remove();
      }
    }
  });
}
function show_contact()
{
  $("#contact_visible").click(
    function(){
        $.ajax({
          url : "/buyandsell/show_contact/no/",
          success: function (data)
          {
            console.log("dont show contact");

          }
        });
      }
      );

      $('#contact_hidden').click(
          function(){
        $.ajax({
          url : "/buyandsell/show_contact/yes/",
          success: function (data)
          {
            console.log("show contact")
          }
        });
      }
    );
    $('#show_contact').click(
        function(){
        if( $(this).hasClass('phone-no-visibility-toggle-button-hidden'))
        {
 $.ajax({
          url : "/buyandsell/show_contact/yes/",
          success: function (data)
          {
            console.log("show contact");

          }
        });
        }
        else
        {
 $.ajax({
          url : "/buyandsell/show_contact/no/",
          success: function (data)
          {
            console.log("dont show contact");

          }
        });
        }

});
}
function watch_subs(id,len_sub)
{
  var elem=$("#"+id);
  var chk=elem.prop("checked");

    //  $("#"+id+"_"+i).prop("checked",chk)
    if(chk==true)
    {
      $("#"+id).addClass("checkbox-custom-to-buyandsell-checked");
      for(var i=1;i<=len_sub;i++)
      {
        $("#" + id + "_" + i).prop("checked", chk);
        $("#" + id + "_" + i).addClass("checkbox-custom-to-buyandsell-checked");
      }
      console.log($(this).class)
    }
    else
    {
      $("#"+id).removeClass("checkbox-custom-to-buyandsell-checked");
      for(var i=1;i<=len_sub;i++)
      {
        $("#"+id+"_"+i).prop("checked",chk);
        $("#" + id + "_" + i).removeClass("checkbox-custom-to-buyandsell-checked");
      }

    }

}
function main_check(id_parent,id,len_sub)
{
  var flag=1;
  var elem= $("#"+id);
  if(elem.prop("checked")==false)
  {
    $("#" + id).removeClass("checkbox-custom-to-buyandsell-checked");
    if ($("#"+id_parent).prop("checked")==true)
    {
      $("#"+id_parent).prop("checked",false);
      $("#"+id_parent).removeClass("checkbox-custom-to-buyandsell-checked");
    }
  }
  else  if(elem.prop("checked")==true)
  {
    $("#" + id).addClass("checkbox-custom-to-buyandsell-checked");
    for(var i=1;i<=len_sub;i++)
    {
      if( $("#"+id_parent+"_"+i).prop("checked")==false)
      {
        flag=0;
      }
    }
    if(flag==1)
    {
      $("#"+id_parent).prop("checked",true);
      $("#"+id_parent).addClass("checkbox-custom-to-buyandsell-checked");
    }
  }
}

$('body').ready(function(){
  $('#id_username').autocomplete({
    source:'/settings/person_search/',
    select:function( event,ui ){
      $('#enroll').val(ui.item.id);
    },
    minLength:1
  });
});

function assign_id(id , type)
{
   if( type == 'sell')
   $("#modal-delete").attr('onclick','trash(' + '"' +type +'"' +','+id + ')' );
   else
   $("#modal-delete-request").attr('onclick','trash(' + '"' +type +'"' +','+id + ')' );

}

show_contact();
search_form();
search();

function sell_form(){
  if(opened_dialog !=""){
    close_dialog(opened_dialog);
  }
  console.log("kanav");
  dialog_iframe({
    name:'sell_form_dialog',
    title:'Sell an Item',
    width:600,
    height:770,
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
    title:'Request an Item',
    width:550,
    height:665,
    src:'/buyandsell/requestitem/',
    close:function(){opened_dialog=""}
  });
  opened_dialog='request_form_dialog';
}

function sell_details(pk,item_name){
  if(opened_dialog !=""){
    close_dialog(opened_dialog);
  }
  $('.search-result-box').hide();
  dialog_iframe({
    name:'sell_detail_dialog',
    title:item_name,
    width:800,
    height:520,
    src:'/buyandsell/sell_details/'+pk+'/',
    close:function(){opened_dialog=""}
  });
  opened_dialog='sell_detail_dialog';
}

function request_details(pk,item_name){
  if(opened_dialog !=""){
    close_dialog(opened_dialog);
  }
  $('.search-result-box').hide();
  dialog_iframe({
    name:'request_detail_dialog',
    title:item_name,
    width:650,
    height:485,
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
    title:'Edit',
    width:600,
    height:770,
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
    title:'Edit Request',
    width:600,
    height:665,
    src:'/buyandsell/edit/request/'+pk+'/',
    close:function(){opened_dialog=""}
  });
  opened_dialog='edit_request_dialog';
}

function manage(){
  console.log(user.is_authenticated);
  check_user_data(user.is_authenticated,user.username);
  if(opened_dialog !=""){
    close_dialog(opened_dialog);
  }
  dialog_iframe({
    name:'manage_watched_categories',
    title:'Manage the Categories you Watch',
    width:600,
    height:400,
    src:'/buyandsell/manage/',
    dialogClass: 'dialog-class buyandsell-manage-dialog',
    close:function(){opened_dialog=""}
  });
  opened_dialog='manage_watched_categories';
}

function transaction_form(type,id){
  if(opened_dialog !=""){
        close_dialog(opened_dialog);

  }
  dialog_iframe({
    name:'trans_form',
    title:'We value your feedback',
    width:800,
    height:600,
    src:'/buyandsell/succ_trans/' + type + '/' + id,
    close:function(){opened_dialog=""}
  });
  opened_dialog='trans_form';
}
function upload_image_buyandsell(unique_name, id){
  uname = unique_name;
if(opened_dialog !=""){
        close_dialog(opened_dialog);

  }
  dialog_iframe({
    name: 'upload_image_dialog',
    title: 'Upload Image',
    width: 700,
    height: 500,
    src: '/crop_image/upload_image/' + unique_name + '/' + id + '/',
    close:function(){opened_dialog="";window.location = "/buyandsell/buy";}
  });
opened_dialog = 'upload_image_dialog';
}

function special_submit(id,type) {
    var form = $("#trans_form");
      form.attr("action" , "/buyandsell/succ_trans/" + type + "/" + id + "/ni/");
      form.submit();
      }

function pic_upload(){
    var form = $("#sell_form");
    $("input[name = upload_pic]").val("no");
    form.submit();
}


function bring_subcats() {
$("#id_category").change(function (){
      var category = $(this).val();
      var url = "/buyandsell/bring_subcats/" + category +"/";
      $.get(url, function(data){
         $("select#sub_category").html(data);
        });
      });
    }
bring_subcats();

$(document).ready
(
  function()
  {
    $(".thumbnailBG").mouseenter
    (
      function()
      {
        $(".edit-button", $(this)).css('opacity', 1);
        $(".dropdown", $(this)).toggle();
        //$(".item-options-dropdown", $(this)).css('display', 'block');
      }
    );

    $(".item-options-dropdown").css('display', 'none');
    $(".thumbnailBG").mouseleave
    (
      function()
      {
        $(".edit-button", $(this)).css('opacity', 0);
        $(".item-options-dropdown", $(this)).removeClass('open');
        $(".dropdown", $(this)).toggle();
      }
    );

    $(".request").mouseenter
    (
      function()
      {
        $(".edit-button", $(this)).css('opacity', 1);
        $(".dropdown", $(this)).toggle();
        //$(".item-options-dropdown", $(this)).css('display', 'block');
      }
    );

    $(".request-options-dropdown").css('display', 'none');
    $(".request").mouseleave
    (
      function()
      {
        $(".edit-button", $(this)).css('opacity', 0);
        $(".request-options-dropdown", $(this)).removeClass('open');
        $(".dropdown", $(this)).toggle();
      }
    );

    $(document).click
    (
      function()
      {

        if($(".item-options-button").attr('aria-expanded')== 'false')
        {
          $(this).hide();
        }

        else if($(".item-options-button").attr('aria-expanded')== 'true')
        {
          $(this).hide();
        }

        else
        {
          console.log("kuchh nahi hua");
        }

        /*
        if (".dropdown", $(this).hasClass("open"))
        {
          $(this).hide();
        }
        else
        {
          // not inside
        }
        */
      }
    );




 /*   $(".request").mouseover
    (
      function()
      {
        $(".edit-button", $(this)).css('opacity', 1);
        $(".request-remove-button", $(this)).css('opacity', 1);
      }
    );
    $(".request").mouseout
    (
      function()
      {
        $(".edit-button", $(this)).css('opacity', 0);
        $(".request-remove-button", $(this)).css('opacity', 0);
      }
    );
*/

    /*
    $(".thumbnailBG-my-account").click
    (
      function() //opens light box with details for the clicked item-for-sale
      {
        //var modalHead = $(".caption .itemName", $(this)).html();
        //console.log(modalHead);
        $(".modal-title").html(modalHead);
        var modalImage = $((".thumbnail img"), $(this)).attr("src");
        //console.log(modalImage);
        $(".modal-image").attr("src",modalImage);
        var modalPrice = $("div .price", $(this)).html();
        //console.log(modalPrice);
        $(".modal-price").html(modalPrice);
      }
    );
    */

  }
);

//Function to center align a div horizontally
jQuery.fn.centerHorizontally = function () {
  this.css("position","absolute");
  this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) +  $(window).scrollLeft()) + "px");
  return this;
}

  //Function to center align a div vertically
  jQuery.fn.centerVertically = function () {
    this.css("position","absolute");
    this.css("top", Math.max(0, (($(window).height() - $(this).outerHeight()) / 2) + $(window).scrollTop()) + "px");
    return this;
  }

  //Function to center align a div both horizontally and vertically
  jQuery.fn.center= function () {
    this.css("position","absolute");
    this.css("top", Math.max(0, (($(window).height() - $(this).outerHeight()) / 2) + $(window).scrollTop()) + "px");
    this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) +  $(window).scrollLeft()) + "px");
    return this;
  }

loadingComplete();
