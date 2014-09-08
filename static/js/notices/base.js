var search_total_pages, search_last_page_notices, search_store;		//variables for search results
var upload_total_pages, upload_last_page_notices, upload_array;		//variables for show_uploads results
var starred_total_pages, starred_last_page_notices, starred_array;		//variables for show_starred results
var total_pages, last_page_notices;		//variables for general new notice display(all)
var old_total_pages, old_last_page_notices;		//variables for general expired notice display(all)
var temp_total_pages, temp_last_page_notices;		//variables for general notice display(specific category)
var store, temp_store, old_store;    //store stands for new store or the store of new notices.
var emptyarray;

var main_mode, sub_mode, m_category, sub_category, cur_page_no, more, name_to_display, all, same_except_page_no, search_string, search_string_changed;
var h1,h2,h3,h4,h5;
/*
  1.Values of sub_mode can be either new or old
  2.same_except_page_no stores if everything is same except the page number
  3.same_except_page_no stores if the newly arrived categories(h3, h4) matches with the old ones
  4.Values of main mode can be display, upload, search, content
  5.The all variable stores if the both the m_category and sub_category are equal to "All" or not.
  6.Initial value of variables in line 10 can't be [display, new, All, All, 1] or ["", "", "", "", ""] because they are supposed to be different from the hashes(#notices and #notice/display/new/All/All/1), that arrive on reload, so that the static divs are created.
*/

var privelege, first_time_visit, static_divs_created, star_perm, select_category, prev_url="#notices/new/All/All/1";
var checklist, check_upload_array, check_star_array, read_array;

/*
    1.check_star_array stores the ids of notices who are starred for a particular user.read_array is similar
    2.search_store stores the results of a particular search
    3.star_perm is 0 when the app is being used anonymously
*/

initialize_global_variables();

function initialize_global_variables()
{
  store = new Array(50);
  temp_store = new Array(50);
  old_store = new Array(50);
  emptyarray = new Array(50);
  all=1;
  same_except_page_no=1;
  main_mode="display";
  sub_mode="";
  m_category="All";
  sub_category="All";
  cur_page_no="1";
  search_string="";
  search_string_changed=0;
  privelege=0; first_time_visit=0; static_divs_created=0; star_perm=0; select_category=0;
  check_upload_array={}; check_star_array={}; read_array={};
}

function first_time_functions()                 //This function is responsible for calling 6 important basic functions to store necessary data
{
    $("#global_search_bar").val("");
    $("#global_search_bar").attr('placeholder', 'Search In Notices');
    get_privelege();                            //First time function 1
}

$(document).on("load_app_notices", function(e, hash1, hash2, hash3, hash4, hash5){

    $("#container").attr({class : "large-width-content"})
    h1=hash1;    //The function redirection can only be called once the first_time_functions have played their part. So, we store the current state variables for now.
    h2=hash2;
    h3=hash3;
    h4=hash4;
    h5=hash5;

    console.log("entered load_app_notices");
    if(first_time_visit==0)
      first_time_functions();
    else
      redirection();
});

$(document).on("unload_app_notices", function(e, hash1, hash2, hash3, hash4, hash5){
    $("#container").removeAttr("class")
    $("#global_search_bar").val("");
    $("#global_search_bar").attr('placeholder', 'Search here');
});

$(document).on("login", function(){
    console.log("login entered");
  if(current_tab=="notices")
  {
    initialize_global_variables();
    first_time_visit=0;
    hashtags = [h1, h2, h3, h4, h5];
    $(document).trigger("load_app_notices", hashtags);
  }
});

$(document).on("logout", function(){
    console.log("logout entered");
  if(current_tab=="notices")
  {
    same_except_page_no=1;
    check_upload_array={}; check_star_array={}; read_array={};
    privelege=0; static_divs_created=0; star_perm=0; select_category=0;
    if(h1!="content")
    {
       create_static_divs();
       static_divs_created=1;
    }
    evaluate_breadcrumbs();
    hashtags = [h1, h2, h3, h4, h5];
    $(document).trigger("load_app_notices", hashtags);
  }
});

$('#global_search_bar').on("keydown", function(event){
        if(event.which==13 && current_tab=="notices")
              {
                      set_search_string();
              }
});

function redirection()            //The main controller function which defines the function path, execution will follow
{
    if(h1 == "content")                              //If the main_mode is content, cut the crap and directly display the notice
    {
        main_mode = "content";
        console.log("display content");
        display_notice(parseInt(h2));
    }
    else
    {
        if(h1=="starred" || h1=="uploads")
        {
          console.log(main_mode);
          console.log(main_mode);
          console.log("asfdghjk");
          if(h1==main_mode)     //Setting the value of the same_except_page_no variable
            same_except_page_no=1;
          else
          {
            $("#category_name").text("All");
            if(h1=="starred")
              $("#app_name").text("Starred Notices");
            else
              $("#app_name").text("Uploaded Notices");
            $("#select_bars").removeAttr("onclick");
            $("#select_bars").attr("onclick", "location.hash = '" + prev_url + "'");
            $("#bars").hide("fade", 200, function(){$("#back").show("fade", 200);});
            $("#filters").slideUp(400);
            same_except_page_no=0;
          }
        }
        else
        {
          if(h1==main_mode && h2==sub_mode && h3==m_category && h4==sub_category)     //Setting the value of the same_except_page_no variable
            same_except_page_no=1;
          else
          {
            $("#app_name").text("Notices");
            $("#select_bars").removeAttr("onclick");
            $("#select_bars").attr("onclick", "display_categories();");
            $("#back").hide("fade", 200, function(){$("#bars").show("fade", 200);});
            $("#filters").slideDown(400);
            same_except_page_no=0;
          }
        }

        if(h1 == undefined || h1 == "")                           //Setting default values to the primary parameters, if they are undefined
        {
          console.log("clicked on 'notices' app");
          h1="display";
          h2="new";
          h3="All";
          h4="All";
          h5="1";
          $("#global_search_bar").val("");
          $("#global_search_bar").attr('placeholder', 'Search In Notices');
          if(static_divs_created==0)
          {
            create_static_divs();
            static_divs_created=1;            //made 1, so that switched_to_notices is not called again, 4 lines later
          }
        }
       
        if(main_mode=="content" && static_divs_created==0)
        {          
            create_static_divs();
        }

        static_divs_created=0;            //made 0, so that switched_to_notices is not called again. Whichever function creates the static divs makes sure that the value of this variable is non-zero, so that the other reasons don't create them again.
        main_mode=h1;                                                //Setting global variables equal to the ones just arrived
        sub_mode=h2;
        m_category=h3;
        sub_category=h4;
        cur_page_no=h5;


        if(m_category=="All"&&sub_category=="All")                          //Setting the value of the all variable
          all=1;
        else
          all=0;

        if(same_except_page_no==0)
          evaluate_breadcrumbs();

        if(sub_mode=="new")                             //coloring the appropriate new old filter
          not_sub_mode="old";
        else
          not_sub_mode="new";
        $('#' + sub_mode + '_button').addClass("active1")
        $('#' + not_sub_mode + '_button').removeClass("active1")
  
        $('#' + sub_mode + '_button').addClass("active1");
        $("#category_menu").remove();
        $("#menu").remove();
        $('#all_select').prop('checked', false);
        checklist={};
        more=0;
        if(sub_category=="All")
          $("#category_name").text(m_category);
        else
          $("#category_name").text(sub_category);

      
        if(main_mode=="display")
        {
              if(same_except_page_no==0)
              {
                if(all==1)
                {
                    if(sub_mode=="new")
                    {
                      temp_store=store;
                      temp_total_pages=total_pages;
                      temp_last_page_notices=last_page_notices;
                    }
                    else
                    {
                      temp_store=old_store;
                      temp_total_pages=old_total_pages;
                      temp_last_page_notices=old_last_page_notices;
                    }
      			        load_numbers_bar(temp_total_pages, ""); //loading the numbers bar, since we already know the total pages,last page notices
                    first_time_check();
                    gap_scanner();                            //Checking for gaps. First 50 notices are already present in temp_array
                }
                else
                {
                    console.log("display all!=1 same_except_page_no=0")
                    temp_store = new Array(50);
                    get_total_notices_no();
      			        load_numbers_bar(temp_total_pages, ""); //loading the numbers bar, since we already know the total pages,last page notices
                    first_time_check();
                    gap_filler_first_time("temp"); //Since temp_store is newly created, it needs to have the first 50 notices. Just call this                                                      function and it'll automatically direct it to gap_scanner() after the first 50 notices                                                        arrive
                }
              }
              else
              {
                  first_time_check();
                  list_notices(parseInt(cur_page_no), temp_store, temp_total_pages, temp_last_page_notices);                                                                                                    //Simply call the list function, if nothing except the page no has changed
              }
        }
        else if(main_mode=="uploads")
        {
            cur_page_no = h2;
            sub_mode = "new";
            m_category = "All";
            sub_category = "All";

            load_numbers_bar(upload_total_pages, "upload_");
            list_notices(parseInt(cur_page_no), upload_array, upload_total_pages, upload_last_page_notices);
        }
        else if(main_mode=="starred")
        {
            sub_mode = "new";
            m_category = "All";
            sub_category = "All";
            cur_page_no = h2;
            
            len = starred_array.length;             //Recalculating parameters, as they might have changed due to addition of star notices
            starred_total_pages=Math.floor(len/10);
            starred_last_page_notices=len%10;
            if(starred_last_page_notices>0)
              starred_total_pages++;
            if(!same_except_page_no)
            {
              $("#filters").slideUp(1000);
            }
            load_numbers_bar(starred_total_pages, "starred_");
            list_notices(parseInt(cur_page_no), starred_array, starred_total_pages, starred_last_page_notices);
        }
        else if(main_mode=="search")
        {
            $("#global_search_bar").val("");
            $("#global_search_bar").attr('placeholder', search_string);
            if(same_except_page_no && !search_string_changed)
            {
              load_numbers_bar(search_total_pages, "search_");
              list_notices(parseInt(cur_page_no), search_store, search_total_pages, search_last_page_notices);
            }
            else
            {
              search_string_changed = 0;
              bring_search_results();
            }
        }
    }
}

/*3 reasons for creation of static divs:
1) "Notices" app is clicked.
2) Notice Board is opened for the first time.
3) Switching from content main_mode to any other notice board main_mode, by pressing back button.
*/

function create_static_divs()                //Create static buttons like upload, new, old, and additional features, when switched
{
    $("#content").empty();
    $("#right-column").empty();
    $('#content').html(welcome_html());
    if(privelege==1)
      $('#notices-header').append(upload_html());
    if(sub_category=="All")
      $('#notices-header').append(load_cat_bar_html(m_category));
    else
      $('#notices-header').append(load_cat_bar_html(sub_category));
    $('#content').append('<div id="filters"></div>');
    $('#filters').append('<div id="breadcrumbs_container"><div id="breadcrumbs"></div></div>');
    $('#filters').append(newold_buttons_html());

    $('#content').append('<div id="additional"></div>');
    if(star_perm==1)
      $('#additional').append(additional_features_html());
    $('#content').append('<div id="notice_list"></div><br>');
    $('#content').append('<div id="page_numbers"></div>')
    console.log("switched_to_noties_create : static divs created")
}

function get_total_notices_no()       //This function is only meant for general notice display(categories other than All, All)
{
  		  $.ajax({
    		  type: 'get',
    		  url : 'notices/temp_max_notices/' + sub_mode + '/' + m_category + '/' + sub_category,
    		  success: function (data)
    		  {
      			temp_last_page_notices = data.total_notices%10;
      			temp_total_pages = Math.floor(data.total_notices/10) ;
      			if (temp_last_page_notices > 0)
        		  temp_total_pages++;
      			load_numbers_bar(temp_total_pages, "");
          }
        });
}

function first_time_check()                                         /* Check if one clicks for the first time on a bundle*/
{
    var bundle_no = parseInt((parseInt(cur_page_no)-1)/5) + 1;
    var len = (temp_store.length/50);
    for(var i=0; i<(bundle_no-len); i++)
      temp_store.push.apply(temp_store, emptyarray);
}

function gap_scanner()                 // Fills the appropriate gaps with notice objects into the store, between indices
{                                                                           // corresponding to the bundle_no.
    console.log("entered_gap_scanner");
    var bundle_no = parseInt((cur_page_no-1)/5) + 1;
    var b = bundle_no*50 -1;
    var i = b - 49;
    var gap_begin = 0, gap_end = 0, temp=0;
    while(i!=b+1)
    {
        if(!(i in temp_store) && temp==0)
        {
          gap_begin = i;
          gap_end = 0;
          temp=1;
        }
        if(temp)
        {
            if(i in temp_store)
              gap_end = i - 1;
            else if(i == b)
              gap_end = i;
            else
            {
              i++;
              continue;
            }
            gap_filler(gap_begin, gap_end, temp_store[0].id);
            gap_begin = 0;
            temp=0;
          }
          i++;
    }
    if(!gap_end)
    {
      console.log("no gaps found");
      list_notices(parseInt(cur_page_no), temp_store, temp_total_pages, temp_last_page_notices);
    }
}

function gap_filler(llim, hlim, temp)
{
        $.ajax({
        type: 'get',
        url : 'notices/list_notices/' + sub_mode + '/' + m_category + '/' + sub_category + '/' + llim + '/' + hlim + '/' + temp,
        success: function (data)
        {
            console.log("entered gap_filler");
            for(var i = llim; i<=hlim; i++)
              temp_store[i] = data[i-llim];
            if(sub_mode=="new")
              store = temp_store;
            else
              old_store = temp_store;
            list_notices(parseInt(cur_page_no), temp_store, temp_total_pages, temp_last_page_notices);
        },
      });
}

function load_numbers_bar(tp, mode1)        //tp = total pages, mode1 = new, old, search, upload
{
      console.log("pagination reset");
      $("#page_numbers").pagination({
          pages: tp,
          currentPage : cur_page_no,
          cssStyle: 'light-theme',
          onPageClick : window[mode1 + 'change_page']
      });
}

function change_page(number)
{
  location.hash = '#notices/display/' + sub_mode +'/' +  m_category + '/' +  sub_category + '/' + number;
}

function open_notice(id)
{
  location.hash = '#notices/content/' + id;
}

function upload_change_page(page_no)
{
  if(main_mode!="uploads" && main_mode!="starred")
    prev_url = location.hash;
  location.hash = '#notices/uploads/' + page_no;
}

function starred_change_page(page_no)
{
  if(main_mode!="uploads" && main_mode!="starred")
    prev_url = location.hash;
  location.hash = '#notices/starred/' + page_no;
}

function search_change_page(page_no)
{
  url_temp = '#notices/search/' + sub_mode + '/' + m_category + '/' + sub_category + '/' + page_no;
  if(location.hash == url_temp)
  {
  	hashtags = ["search", sub_mode, m_category, sub_category, String(page_no)];
  	$(document).trigger("load_app_notices", hashtags);
  }
  else
  {
	  location.hash=url_temp;
  }
}

function list_notices(page_no, tstore, ttotal_pages, tlast_page_notices)    //t here stands for temp, representing the local variables
{
      console.log("entered list_notices : " + page_no);
      $('div#notice_list').empty();
      var k = 0;
      if(page_no < ttotal_pages || (page_no == ttotal_pages && tlast_page_notices==0))
        k = 10;
      else
        k = tlast_page_notices;
      var a=(page_no-1)*10, b=a+k;
      context = {};
      for(var i=a; i<b; i++)
      {
            context["notice"] = tstore[i];

            if(star_perm==1)
              context["anonymous"] = 0;
            else
              context["anonymous"] = 1;

            if(check_upload_array[tstore[i].id]==1)
              context["edit"] = 1;
            else
              context["edit"] = 0;

            if(read_array[tstore[i].id]==1)
              context["read"] = 1;
            else
              context["read"] = 0;

            if(check_star_array[tstore[i].id]==1)
              context["star"] = 1;
            else
              context["star"] = 0;

            $('#notice_list').append(list_notices_html(context));

      }
      $(".notice_date").each(function() {
              $(this).text($(this).text().substr(0,10));
              });
}

function display_notice(id)
{
  read_notice(id);
  $.ajax({
    type: 'get',
    url : 'notices/get_notice/' + id,
    success: function(data)
    {
      $('#content').empty();
      $('#content').append(display_notice_html(data));
    },
    error: function(data)
    {
      html = ("Error");
      $('#content').empty();
      $('#content').append(html);
    }
  });
}

function set_search_string()
{
      console.log("entered search");
      if($("#global_search_bar").val()!=search_string)
        search_string_changed=1;
      search_string = $("#global_search_bar").val();
/*      if(search_bar_value=="")
      {
        search_bar_value=search_string;
      }
*/
      search_change_page(1);
}

function check_if_date()
{
      console.log("entered check_if_date")
      url=""
      if(search_string.split("-").length==2)
      {
        parts=search_string.split("-");
        parts[0]=Date.parse(parts[0]);
        parts[1]=Date.parse(parts[1]) + 86400000;
        console.log(parts[1]);
        if(parts[0]>1262284200000 && parts[1]>1262284200000)
        url = ">>" + parts.join().replace(",", "-");
      }
      else if(!isNaN(Date.parse(search_string)) && Date.parse(search_string)>1262284200000)
      {
        x = Date.parse(search_string)
        url = ">>" + x.toString() + "-" + (x+86400000).toString();
      }
      console.log(url);
      return url
}
function bring_search_url()
{
      url = check_if_date();
      if(url=="")
      {
          if(search_string=="")
            return ""
          query=search_string.split(" ");
          t=0;
          k=query.length;
          for(var i=0; i<k;i++)
          {
            if(query[t]=="")
              query.splice(t,1);
            else
              t++;
          }
          for(var i=0; i<query.length-1; i++)
          {
            url+=query[i]+"+";
          }
          url+=query[query.length-1];
      }
      return url;
}

function bring_search_results()
{
      url = bring_search_url();
      console.log(url);
      $.ajax({
          type: 'get',
          url : 'notices/search/' + sub_mode + '/' + m_category + '/' + sub_category + '/?q=' + url,
          success: function (data)
          {
            len=Object.keys(data).length;
            search_total_pages=Math.floor(len/10);
            search_last_page_notices=len%10;
            if(search_last_page_notices>0)
              search_total_pages++;
            search_store = new Array(len);
            search_store = data;
            console.log("search_done");
            console.log(search_store);
            console.log("search_ends");
            load_numbers_bar(search_total_pages, "search_");
            list_notices(parseInt(cur_page_no), search_store, search_total_pages, search_last_page_notices);
          }
        });
}

function star_notice(id, e)
{
      if(e.stopPropagation)
          e.stopPropagation();
        else
          e.cancelBubble = true;
      if(check_star_array[id]==1)
      {

        len = starred_array.length;
        for(var i=0; i<len; i++)
          if(starred_array[i].id==id)
          {
              starred_array.splice(i,1);
              break;
          }

        url = 'notices/read_star_notice/'+id+'/'+'remove_starred';
        delete check_star_array[id];
          $("#star_shape_" + id).attr({style : "color:#AAA"});
      }
      else
      {
        url = 'notices/read_star_notice/'+id+'/'+'add_starred';
        check_star_array[id]=1;

        if(main_mode=="display")
          store_to_use = temp_store;
        else if(main_mode=="search")
          store_to_use = search_store;
        else if(main_mode=="uploads")
          store_to_use = upload_array;
        else if(main_mode=="starred")
          store_to_use = starred_array;

        len = store_to_use.length;
        for(var i=0; i<len; i++)
          if(store_to_use[i].id==id)
          {
              insert_and_maintain_datesort(store_to_use[i]);
              break;
          }
        check_star_array[id] = 1;
        $("#star_shape_" + id).attr({style : "color:#F1C40F"})
      }
      $.ajax({
      type: 'post',
      url: url,
      error : function()
      {
        html = 'Error';
        $('#content').empty();
        $('#content').append(html);
      }
      });
}

function read_notice(id)
{
	if(!(id in read_array))
	{
		url = 'notices/read_star_notice/'+id+'/'+'add_read';
		read_array[id]=1;
	  $.ajax({
	  type: 'post',
	  url: url
	  });
  }
}

function edit_notice(id, e)
{
  window.location.href = 'notices/edit_notice/'+id;
	if(e.stopPropagation)
    	e.stopPropagation();
  	else
    	e.cancelBubble = true;
}

function delete_notice(id, e)
{
  var r = confirm("Are you sure you want to delete this Notice? Once Deleted, the Notice cannot be recovered!");
  if(r==true)
  {
    window.location.href = 'notices/delete_notice/'+id;
  }
	  if(e.stopPropagation)
      e.stopPropagation();
  	else
    	e.cancelBubble = true;
}

function add_to_checklist(id, e)
{
  console.log("gaind7");
  var x = document.getElementById("check-" + id).checked;
  if(!x)
    delete checklist[id];
  else
    checklist[id]=1;
	if(e.stopPropagation)
    e.stopPropagation();
  else
    e.cancelBubble = true;
}

function select_all()
{
    //$('#all_select').click();
    var x = document.getElementById("all_select").checked;
    var k,mode_prefix;

    if(main_mode=="display")
        mode_prefix="temp";
    else if(main_mode=="uploads")
        mode_prefix="upload";
    else if(main_mode=="search")
        mode_prefix="search";
    else if(main_mode=="starred")
        mode_prefix="starred";

    if(parseInt(cur_page_no)<window[mode_prefix + "_total_pages"]||window[mode_prefix + "_last_page_notices"]==0)
      k=10;
    else
      k=window[mode_prefix + "_last_page_notices"];
    console.log(x);
    if(x)
    {
        $('.check').prop('checked', true);
        for(var i=0; i<k; i++)
        {
            id = $('.check')[i].id[6]+$('.check')[i].id[7];
            checklist[parseInt(id)]=1;
        }
    }
    else
    {
        $('.check').prop('checked', false);
        for(var i=0; i<k; i++)
        {
            id = $('.check')[i].id[6]+$('.check')[i].id[7];
            delete checklist[parseInt(id)];
        }
    }
}

function show_menu(e)
{
    if(e.stopPropagation)
      e.stopPropagation();
    else
      e.cancelBubble = true;
    if(more==1)
    {
      $("#more").css("background-color", "#E7E7E7");
      $("#menu").remove();
      more=0;
    }
    else
    {
      $("#more").css("background-color", "#97968D");
      $('#super_more').append(more_html());
      more=1;
    }
}

function insert_and_maintain_datesort(notice)
{
  console.log(notice);
   len = starred_array.length
     if(len==0)
       starred_array.push(notice);
     else if(len==1)
     {
         if(notice.datetime_modified>=starred_array[0].datetime_modified)
          starred_array.splice(0, 0, notice);
         else
          starred_array.splice(1, 0, notice);
     }  
     else
     {
       if(notice.datetime_modified>=starred_array[0].datetime_modified)
        starred_array.splice(0, 0, notice);
       else if(notice.datetime_modified<=starred_array[len-1].datetime_modified)
        starred_array.splice(len, 0, notice);
       else
       {
         for(var i=1;i<len;i++)
           if(notice.datetime_modified<=starred_array[i-1].datetime_modified && notice.datetime_modified>=starred_array[i].datetime_modified)
           {
             starred_array.splice(i, 0, notice);
             break;
           }
       }
     }
}

function read_star_checklist(t)
{
    console.log("entered read_star_checklist t :" + t);
    a = Object.keys(checklist);
    console.log(a);
    k=a.length;
    url = 'notices/mul_read_star_notice/';
    var q = "?q=";
    store_to_use = [];
    if(main_mode=="display")
      store_to_use = temp_store;
    else if(main_mode=="search")
      store_to_use = search_store;
    else if(main_mode=="uploads")
      store_to_use = upload_array;
    else if(main_mode=="starred")
      store_to_use = starred_array;

    for(var i=0;i<k;i++)
    {
      q += a[i]+'+';
      if(t==1)
      {
        if(check_star_array[a[i]]==1)
          continue;
        len = store_to_use.length;
        for(var m=0; m<len; m++)
          if(store_to_use[m].id==a[i])
          {
              insert_and_maintain_datesort(store_to_use[m]);
              break;
          }
        
        check_star_array[a[i]]=1;
        $("#star_shape_" + a[i]).attr({style : "color:#F1C40F"})
      }
      else if(t==2)
      {
        console.log(a[i]);
        if(check_star_array[a[i]]==undefined)
          continue;

        len = starred_array.length;
        for(var m=0; m<len; m++)
          if(starred_array[m].id==a[i])
          {
              starred_array.splice(m,1);
              break;
          }

        delete check_star_array[a[i]];
        $("#star_shape_" + a[i]).attr({style : "color: #AAA"})
      }
      else if(t==3)
      {
        read_array[a[i]]=1;
        $("#notice_"+a[i]).attr({class : "notice_info read"});
      }
      else
      {
        delete read_array[a[i]];
        $("#notice_"+a[i]).attr({class : "notice_info unread"});
      }
    }
    q=q.substring(0,q.length-1);
    if(t==1)
      url += 'add_starred/';
    if(t==2)
      url += 'delete_starred/';
    if(t==3)
      url += 'add_read/';
    if(t==4)
      url += 'delete_read/';
    $.ajax({
      type: 'post',
      url: url+q,
      error : function()
      {
        $('#content').empty();
        $('#content').append('Error');
      }
    });
}

function display_categories()
{
  console.log("hello");
  if(select_category==0)
  {
    $('#select_bars').css("color", "#DD4B39")
    $('#button_category_app_name').append(display_categories_html());
    select_category=1;
  }
  else
  {
    $('#select_bars').css("color", "#666666")
    $('#category_menu').remove();
    select_category=0;
  }
}

function display_sub_categories(main_category)
{
  var len=constants[main_category].length;
  var k=Math.min(len, 11)
  $('#category_child1').empty(); $('#category_child2').empty();
  $('#category_child1').append(display_sub_categories_html(0, k, main_category));
  $('#category_child2').append(display_sub_categories_html(k, len, main_category));
}

function change_category_bar_name(main_category, category)
{
    console.log("entered change_category_bar_name")
    $('#category_menu').remove();
    select_category=0;
    if(m_category==main_category && sub_category==category)
      return;
    select_category=0;
    url_temp = '#notices/' + main_mode + '/' + sub_mode + '/' + main_category +'/' +  category + '/1';
    location.hash = url_temp;
}

function newold_clicked(ns)       //ns stands for new status, storing the sub_mode of the button that is clicked.
{
    console.log("entered newold_clicked");
    if(sub_mode!=ns)
    {
      url_temp = '#notices/' + main_mode + '/' + ns + '/' + m_category +'/' +  sub_category + '/1';
      location.hash = url_temp;
    }
}

function evaluate_breadcrumbs()
{
    if(sub_mode=="new")
      notice_prefix = "Current"
    if(sub_mode=="old")
      notice_prefix = "Expired"

    if(main_mode=="display")
    {
      if(all==1)
      create_breadcrumbs(notice_prefix + "Notices", "All", 1);
      else
      create_breadcrumbs(notice_prefix + "Notices", m_category, sub_category, 1);
    }
    else if(main_mode=="search")
    {
      if(all==1)
        create_breadcrumbs("SearchedNotices", notice_prefix, "All", 0);
      else
        create_breadcrumbs("SearchedNotices", notice_prefix, m_category, sub_category, 0);
    }
}

function create_breadcrumbs()
{
  console.log("entered : create_breadcrumbs");
  console.log(arguments[0] + arguments[1] + arguments[2]);
  $('#breadcrumbs').empty();
  var code = arguments[arguments.length-1];
  for (var i = 0; i < arguments.length-2; i++) 
  {
      $('#breadcrumbs').append(create_breadcrumb_html(arguments[i], code));
      $('#breadcrumbs').append('<i class="fa fa-angle-right breadcrumb_i"><i> ');
      code++;
  }
  $('#breadcrumbs').append(create_breadcrumb_html(arguments[arguments.length-2], 3));
}

function breadcrumb_clicked(tag_type)
{
  console.log(tag_type);
  url = "";
  if(tag_type==0)                                             //coded 0 : main_mode
    url = '#notices/' + main_mode + '/new/All/All/1'
  if(tag_type==1)                                              //coded 1 : sub_mode
    url = '#notices/' + main_mode + '/' + sub_mode + '/All/All/1'
  if(tag_type==2)                                            //coded 2 : m_category
    url = '#notices/' + main_mode + '/' + sub_mode + '/' + m_category + '/All/1'
  if(tag_type!=3)
  location.hash = url;
}

//Following are the functions that are called the first time, notices is clicked

function get_privelege()
{
		$.ajax({
    		type: 'get',
    		url : 'notices/privelege/',
    		success: function (data)
    		{
			      star_perm=1;
      			if(data.privelege)
      			{
				      privelege=1;
              bring_uploads();                         //First time function 2, in case user is an uploader
      			}
            else
              bring_starred_notices();                   //First time function 2, in case user is logged in and not an uploader
            console.log("loaded get_privelge : privelege: " + privelege + " star_perm : " + star_perm)
    		},
        error: function (data)
        {
            get_total_notices_no_first_time();          //First time function 2, in case of anonymous user
            console.log("loaded get_privelge : anonymous")
        }
  });
}

function get_total_notices_no_first_time()
{
  		  $.ajax({
    		  type: 'get',
    		  url : 'notices/max_notices/',
    		  success: function (data)
    		  {
      			  last_page_notices = data['total_new_notices']%10;
      			  total_pages = Math.floor(data['total_new_notices']/10) ;
      			  if (last_page_notices > 0)
        		    total_pages++;
              old_last_page_notices = data['total_old_notices']%10;
      			  old_total_pages = Math.floor(data['total_old_notices']/10) ;
              if (old_last_page_notices > 0)
        		    old_total_pages++;
              console.log("loaded : total_notices_no old and new");
              get_constants();
          }
          });
}

function get_constants()      			// A function that brings all main_categories and sub_categories
{
        $.ajax({
        type: 'get',
        url: 'notices/get_constants/',
        success: function(data)
        {
          constants = data;
          console.log(data);
          console.log("loaded : get_constants");
          gap_filler_first_time("new");
        }
        });
}

function bring_starred_notices()      			// A function that brings all the starred notice corresponding to a particular user
{
	$.ajax({
	type: 'get',
	url: 'notices/star_notice_list/',
	success: function(data)
	{
		len = Object.keys(data).length;
    starred_array = new Array(len);
		for(var i=0;i<len;i++)
		{
      starred_array[i] = data[i];
			check_star_array[data[i].id]=1;
		}
    console.log("loaded : starred_notices");
    bring_read_notices();                 //First time function 4, in case user is an uploader
                                          //First time function 3, in case user is logged in and not an uploader
	}
	});
}

function bring_read_notices()      			// A function that brings all the read notice corresponding to a particular user
{
	$.ajax({
	type: 'get',
	url: 'notices/read_notice_list/',
	success: function(data)
	{
		len = Object.keys(data).length;
		for(var i=0;i<len;i++)
    {
			read_array[data[i]]=1;
		}
    console.log("loaded : read_notices");
    get_total_notices_no_first_time();      //First time function 5, in case user is an uploader
                                        // and function 4, in case user is logged in and not an uploader
	}
	});
}

function bring_uploads()
{
   $.ajax({
      type: 'get',
      url: 'notices/show_uploads/',
      success: function(data)
      {
        len = Object.keys(data).length;
		    upload_total_pages=Math.floor(len/10);
        upload_last_page_notices=len%10;
        if(upload_last_page_notices>0)
        upload_total_pages++;
        upload_array = new Array(len);
        for(var i=0;i<len;i++)
        {
          upload_array[i] = data[i];
          check_upload_array[data[i].id]=1;
        }
        upload_array.sort(function(a, b){
           var dateA=new Date(a.datetime_modified), dateB=new Date(b.datetime_modified);
            return dateB-dateA; //sort by date descending
        })
        console.log("loaded : bring_uploads");
        bring_starred_notices();              //First time function 3, in case user is an uploader
      }
   });
}

function gap_filler_first_time(bring_what)
{

        if(bring_what=="new")
          url = 'notices/list_notices/new/All/All/0/49/0';
        else if(bring_what=="old")
          url = 'notices/list_notices/old/All/All/0/49/0';
        else
          url = 'notices/list_notices/' + sub_mode + '/' + m_category + '/' + sub_category + '/0/49/0';

        $.ajax({
        type: 'get',
        url : url,
        success: function (data)
        {
           for(var i = 0; i<=49; i++)
           {
                if(bring_what=="new")
                  store[i] = data[i];
                else if(bring_what=="old")
                  old_store[i] = data[i];
                else if(bring_what=="temp")
                {
                  temp_store[i] = data[i];
                }
           }
           console.log("loaded : gap_filler_first_time : " + bring_what);

           if(bring_what=="temp")
              gap_scanner();          //If the mode is temp, go to normal gap_filler(specially made for this purpose) and scan again for gaps.
           if(bring_what=="new")
              gap_filler_first_time("old");             //First time function 6, in case user is an uploader
                                                        //First time function 5, in case user is logged in and not an uploader
                                                        //First time function 3, in case user is anonymous
           if(bring_what=="old")
           { 
             if(h1!="content")
             {
               create_static_divs();
               static_divs_created=1;
             }
             first_time_visit=1;
             redirection();
           }
        }
        });
}
 
//Following are the functions which bring html from .hbs files

function welcome_html()
{
      return Handlebars.notices_templates.welcome();
}

function upload_html()
{
    return Handlebars.notices_templates.upload();
}

function load_cat_bar_html(name)
{
    console.log("name : " + name + sub_category)
    return Handlebars.notices_templates.load_cat_bar({name : name});
}

function additional_features_html()
{
    return Handlebars.notices_templates.additional_features();
}

function newold_buttons_html()
{
    return Handlebars.notices_templates.newold_buttons();
}

function load_numbers_bar_html(tp23, mode1)
{
    numbers = [];
    for(var i=1;i<tp23;i++)numbers.push(i);
    return Handlebars.notices_templates.load_numbers_bar({ tp : tp23 , numbers : numbers, mode1 : mode1});
}

function display_notice_html(data)
{
    return Handlebars.notices_templates.display_notice({data : data});
}

function more_html()
{
    return Handlebars.notices_templates.more();
}

function display_categories_html(a)
{
    var a = Object.keys(constants);
    return Handlebars.notices_templates.display_categories({a : a});
}

function display_sub_categories_html(initi, finali, main_category)
{
    sub_categories = {};
    for(var i=initi;i<finali;i++)
    {
      sub_categories[i] = constants[main_category][i];
    }
    return Handlebars.notices_templates.display_sub_categories({ sub_categories : sub_categories , main_category : main_category});
}

function list_notices_html()
{
    return Handlebars.notices_templates.list_notices(context);
}

function create_breadcrumb_html(tag, code)
{
    return Handlebars.notices_templates.create_breadcrumb({tag : tag, code : code});
}

$(window).load(function(){

$(".notice_date").each(function() {
        $(this).text($(this).text().substr(0,10));
        });
}
);
