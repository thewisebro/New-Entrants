var search_total_pages, search_last_page_notices, search_store;		//variables for search results
var upload_total_pages, upload_last_page_notices, upload_array;		//variables for show_uploads results
var starred_total_pages, starred_last_page_notices, starred_array;		//variables for show_starred results
var total_pages, last_page_notices;		//variables for general new notice display(all)
var old_total_pages, old_last_page_notices;		//variables for general expired notice display(all)
var temp_total_pages, temp_last_page_notices;		//variables for general notice display(specific category)
var store, temp_store, old_store;    //store stands for new store or the store of new notices.
var emptyarray;

var main_mode, sub_mode, m_category, sub_category, cur_page_no, store_to_use, more, name_to_display, all, same_except_page_no, search_string, search_string_changed, prev_content_url, content_button_state, no_notices, binding_done;
var h1,h2,h3,h4,h5;
/*
  1.Values of sub_mode can be either new or old
  2.same_except_page_no stores if everything is same except the page number
  3.same_except_page_no stores if the newly arrived categories(h3, h4) matches with the old ones
  4.Values of main mode can be display, upload, search, content
  5.The all variable stores if the both the m_category and sub_category are equal to "All" or not.
  6.Initial value of variables in line 10 can't be [display, new, All, All, 1] or ["", "", "", "", ""] because they are supposed to be different from the hashes(#notices and #notice/display/new/All/All/1), that arrive on reload, so that the static divs are created.
  7.Pre variables store the state of the app before someone goes in content mode.
  8.binding_done stores if the binding is done with the "Actions" div.
*/

var privelege, first_time_visit, static_divs_created, star_perm, select_category, prev_url;
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
  no_notices=0;
  binding_done=0;
//  same_except_page_no=1;
  main_mode="display";
  sub_mode="";
  m_category="All";
  sub_category="All";
  cur_page_no="1";
  search_string="";
  search_string_changed=0;
  privelege=0; first_time_visit=0; static_divs_created=0; star_perm=0; select_category=0;
  check_upload_array={}; check_star_array={}; read_array={};
  prev_url="#notices/display/new/All/All/1";
  prev_content_url="#notices/display/new/All/All/1";
}

function first_time_functions()                 //This function is responsible for calling 6 important basic functions to store necessary data
{
    $("#search-inp").val("");
    $("#search-inp").attr('placeholder', 'Search notices');
    get_privelege();                            //First time function 1
}

$(document).on("load_app_notices", function(e, hash1, hash2, hash3, hash4, hash5){

    //console.log("entered load_app_notices");
    h1=hash1;    //The function redirection can only be called once the first_time_functions have played their part. So, we store the current state variables for now.
    h2=hash2;
    h3=hash3;
    h4=hash4;
    h5=hash5;

    if(first_time_visit==0)
      first_time_functions();
    else
      redirection();
});

$(document).on("unload_app_notices", function(e, hash1, hash2, hash3, hash4, hash5){

    $("#container").removeAttr("class")
    $("#search-inp").attr('placeholder', 'Search notices');
    $("#content").empty();
});

$(document).ready(function() {
    //console.log("asidashdiuasdsaduiashdiusadads");
$("#show_starred").tooltip({
  position: {
      my: "right bottom+50",
      at: "right top"
    }
  });
});

$(document).on("login", function(){
    //console.log("login entered");
  if(nucleus.get_current_app()=="notices")
  {
    initialize_global_variables();
    first_time_visit=0;
    hashtags = [h1, h2, h3, h4, h5];

    $(document).trigger("load_app_notices", hashtags);
  }
});

$(document).on("logout", function(){
    //console.log("logout entered");
  if(nucleus.get_current_app()=="notices")
  {
    same_except_page_no=1;
    check_upload_array={}; check_star_array={}; read_array={};
    privelege=0; star_perm=0;
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

function redirection()            //The main controller function which defines the function path, execution will follow
{
    $("#container").addClass("large-width-content");
    if(h1 == "content")                              //If the main_mode is content, cut the crap and directly display the notice
    {
        $("#content").empty();
        $("#right-column .content").empty();
        $('#content').html(welcome_html());
        if(privelege==1)
          $('#notices-header').append(upload_html());
        if(sub_category=="All")
          $('#notices-header').append(load_cat_bar_html(m_category));
        else
          $('#notices-header').append(load_cat_bar_html(sub_category));
        $('#notices-header').append(search_bar_html());
        $('#content').append('<div id="filters"></div>');
        $('#filters').append('<div id="breadcrumbs_container"><div id="breadcrumbs"></div></div>');
        $('#filters').append(prev_next_buttons_html());
        $('#content').append('<div style="clear:both"></div>');
        //console.log("display content");
        main_mode = "content";
        $("#select_bars").removeAttr("onclick");
        $("#select_bars").attr("onclick", "location.hash = '" + prev_url + "'");
        $("#bars").hide("fade", 200, function(){$("#back").show("fade", 200);});
        evaluate_breadcrumbs();
        display_notice(parseInt(h2));
    }
    else
    {

        if(main_mode=="content" && static_divs_created==0)
        {
          //console.log("23starred_uploads_yes");
            create_static_divs();
        }

        if(h1=="starred" || h1=="uploads")
        {
          //console.log("1starred_uploads_yes");
          if(h1==main_mode)     //Setting the value of the same_except_page_no variable
            same_except_page_no=1;
          else
          {
          //console.log("2starred_uploads_yes");
          //console.log(h1);
            $("#category_name").text("All");
          //console.log("3starred_uploads_yes");
            if(h1=="starred")
            {
              //console.log("10starred_uploads_yes");
              $("#app_name").text("Starred Notices");
            }
            else
              $("#app_name").text("Uploaded Notices");
          //console.log("5starred_uploads_yes");
            $("#select_bars").removeAttr("onclick");
            $("#select_bars").attr("onclick", "location.hash = '" + prev_url + "'");
          //console.log("6starred_uploads_yes");
            $("#bars").hide("fade", 200, function(){$("#back").show("fade", 200);});
            $("#filters").slideUp(400);
          //console.log("7starred_uploads_yes");
            same_except_page_no=0;
          }
        }
        else
        {
          //console.log("2332starred_uploads_yes");
          if(h1==main_mode && h2==sub_mode && h3==m_category && h4==sub_category)     //Setting the value of the same_except_page_no variable
            same_except_page_no=1;
          else
          {
            $("#app_name").text("Notices");
            $("#select_bars").removeAttr("onclick");
            $("#select_bars").attr("onclick", "display_categories(event);");
            $("#back").hide("fade", 200, function(){$("#bars").show("fade", 200);});
            $("#filters").slideDown(400);
            same_except_page_no=0;
          }
        }

        if(h1 === undefined || h1 === "")                           //Setting default values to the primary parameters, if they are undefined
        {
          //console.log("clicked on 'notices' app");
          h1="display";
          h2="new";
          h3="All";
          h4="All";
          h5="1";
          $("#search-inp").val("");
          if(static_divs_created==0)
          {
            create_static_divs();
            static_divs_created=1;            //made 1, so that switched_to_notices is not called again, 4 lines later
          }
        }
        if($("#notices-header")[0]==undefined)
        {
            create_static_divs();
            static_divs_created=1;            //made 1, so that switched_to_notices is not called again, 4 lines later
        }

        static_divs_created=0;            //made 0, so that switched_to_notices is not called again. Whichever function creates the static divs makes sure that the value of this variable is non-zero, so that the other reasons don't create them again.
        main_mode=h1;                                                //Setting global variables equal to the ones just arrived
        sub_mode=h2;
        //console.log("idhar hua tha")
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
        $("#search-inp").attr('placeholder', 'Search notices');

      
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
                    if(temp_total_pages!=0)
                    {
                      first_time_check();
                      gap_scanner();                            //Checking for gaps. First 50 notices are already present in temp_array
                    }
                }
                else
                {
                    //console.log("display all!=1 same_except_page_no=0");
                    temp_store = new Array(50);
                    get_total_notices_no();
                }
                store_to_use = temp_store;
              }
              else
              {
	          //console.log("here it is1");
                  first_time_check();
                  var check1;
                  for(check1=(cur_page_no-1)*10;check1<cur_page_no*10;check1++)
                  {
                    if(!(check1 in temp_store) || temp_store[check1]==undefined)
                    {
		      //console.log("here it is");
                      gap_scanner();                            //Checking for gaps. First 50 notices are already present in temp_array
                      //console.log("yes" + check1);
                      break;
                    }
                  }
                  if(check1 == cur_page_no*10)
                  {
                      //console.log("no");
                      list_notices(parseInt(cur_page_no), temp_store, temp_total_pages, temp_last_page_notices);
                  }
              }
        }
        else if(main_mode=="uploads")
        {
            cur_page_no = h2;
            sub_mode = "new";
            m_category = "All";
            sub_category = "All";
            store_to_use = upload_array;

            load_numbers_bar(upload_total_pages, "upload_");
            if(upload_total_pages!=0)
              list_notices(parseInt(cur_page_no), upload_array, upload_total_pages, upload_last_page_notices);
        }
        else if(main_mode=="starred")
        {
            sub_mode = "new";
            m_category = "All";
            sub_category = "All";
            cur_page_no = h2;
            store_to_use = starred_array;
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
            if(starred_total_pages!==0)
              list_notices(parseInt(cur_page_no), starred_array, starred_total_pages, starred_last_page_notices);
        }
        else if(main_mode=="search")
        {
            $("#search-inp").val(search_string);
            if(same_except_page_no && !search_string_changed)
            {
              load_numbers_bar(search_total_pages, "search_");
              if(search_total_pages!==0)
                list_notices(parseInt(cur_page_no), search_store, search_total_pages, search_last_page_notices);
            }
            else
            {
              //console.log("calling bring_search_results");
              search_string_changed = 0;
              bring_search_results();
            }
        }
        if($("#breadcrumbs")[0].innerHTML=="")
          evaluate_breadcrumbs();
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
    $("#right-column .content").empty();
    $('#content').html(welcome_html());
    if(privelege==1)
      $('#notices-header').append(upload_html());
    if(sub_category=="All")
      $('#notices-header').append(load_cat_bar_html(m_category));
    else
      $('#notices-header').append(load_cat_bar_html(sub_category));
    $('#notices-header').append(search_bar_html());
    $('#content').append('<div id="filters"></div>');
    $('#filters').append('<div id="breadcrumbs_container"><div id="breadcrumbs"></div></div>');
    $('#filters').append(newold_buttons_html());
    $('#content').append('<div style="clear:both"></div>');

    $('#content').append('<div id="additional"></div>');
    if(star_perm==1)
      $('#additional').append(additional_features_html());
    $('#content').append('<div id="notice_list"></div><br>');
    if(star_perm!=1)
      $('#content').append('<div id="page_numbers-subscription-wrap"><div id="page_numbers"></div><div style="clear:both"></div></div>');
    else
      $('#content').append('<div id="page_numbers-subscription-wrap"><div id="page_numbers"></div><div id="settings" onclick="location.hash=\'#settings/email\'"><i id="gear" class="fa fa-cog"></i>Subscription Settings</div><div style="clear:both"></div></div>');
    //console.log("switched_to_notices_create : static divs created");
    $('#more').bind("click", bind_unbind_tooltip);
}

function get_total_notices_no()       //This function is only meant for general notice display(categories other than All, All)
{
      $.ajax({
        type: 'get',
        url : 'notices/temp_max_notices/' + sub_mode + '/' + m_category + '/' + sub_category + '/',
        success: function (data)
        {
          temp_last_page_notices = data.total_notices%10;
          temp_total_pages = Math.floor(data.total_notices/10) ;
          if (temp_last_page_notices > 0)
            temp_total_pages++;
          load_numbers_bar(temp_total_pages, "");
          if(temp_total_pages!==0)
          {
              first_time_check();
              gap_filler_first_time("temp"); //Since temp_store is newly created, it needs to have the first 50 notices. Just call this                                                      function and it'll automatically direct it to gap_scanner() after the first 50 notices                                                        arrive
          }
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
    //console.log("entered_gap_scanner");
    var bundle_no = parseInt((cur_page_no-1)/5) + 1;
    var b = bundle_no*50 -1;
    var i = b - 49;
    var gap_begin = 0, gap_end = 0, temp=0;
    while(i!=b+1)
    {
        if((!(i in temp_store) || temp_store[i]==undefined) && temp==0)
        {
          gap_begin = i;
          gap_end = 0;
          temp=1;
        }
        if(temp)
        {
            if(i in temp_store && temp_store[i]!=undefined)
	    {
		    //console.log("enter");
              gap_end = i - 1;
	      gap_filler(gap_begin, gap_end, temp_store[0].id);
	      gap_begin = 0;
	      temp=0;
	    }
            else if(i == b)
	    {
		    //console.log("enter1");
		    //console.log($("#page_numbers ul")[0]==undefined);
              gap_end = i;
	      gap_filler(gap_begin, gap_end, temp_store[0].id);
	      gap_begin = 0;
	      temp=0;
	    }
            else
            {
              i++;
              continue;
            }
          }
          i++;
    }
    if(!gap_end)
    {
      //console.log("no gaps found");
      if(main_mode!="content")
        list_notices(parseInt(cur_page_no), temp_store, temp_total_pages, temp_last_page_notices);
      else
        prev_next_clicked(-1);         //This function is also called, while clicking next in content mode
    }
}

function gap_filler(llim, hlim, temp)
{
        $.ajax({
        type: 'get',
        url : 'notices/list_notices/' + sub_mode + '/' + m_category + '/' + sub_category + '/' + llim + '/' + hlim + '/' + temp + '/',
        success: function (data)
        {
            //console.log("entered gap_filler");
            for(var i = llim; i<=hlim; i++)
              temp_store[i] = data[i-llim];
            store_to_use = temp_store;
            if(m_category=="All" && sub_category=="All")
            {
              if(sub_mode=="new")
                store = temp_store;
              else
                old_store = temp_store;
            }
            if(main_mode!="content")            //This function is also called, while clicking next in content mode
              list_notices(parseInt(cur_page_no), temp_store, temp_total_pages, temp_last_page_notices);
            else
              prev_next_clicked(content_button_state);
        },
      });
}

function load_numbers_bar(tp, mode1)        //tp = total pages, mode1 = new, old, search, upload
{
      //console.log("pagination reset");
      //console.log("tp : " + tp);
      $("#settings").show();
      if(tp!==0)
      {
      //console.log("1pagination reset");
        $("#page_numbers").pagination({
            pages: tp,
            currentPage : cur_page_no,
            cssStyle: 'light-theme',
            onPageClick : window[mode1 + 'change_page']
        });
      }
      else
      {
        $("#page_numbers").empty();
        $("#settings").hide();
        write_no_notices_yet();
      }
}

function change_page(number)
{
  location.hash = '#notices/display/' + sub_mode +'/' +  m_category + '/' +  sub_category + '/' + number;
}

function open_notice(id)
{
  if(main_mode!="content")
    prev_content_url = location.hash;
  if(prev_content_url=="#notices")
    prev_content_url = '#notices/display/new/All/All/1';
  location.hash = '#notices/content/' + id;
}

function upload_change_page(page_no)
{
  if(main_mode!="uploads" && main_mode!="starred")
    prev_url = location.hash;
  if(prev_url=="#notices")
    prev_url = '#notices/display/new/All/All/1';
  location.hash = '#notices/uploads/' + page_no;
}

function starred_change_page(page_no)
{
  if(main_mode!="uploads" && main_mode!="starred")
    prev_url = location.hash;
  if(prev_url=="#notices")
    prev_url = '#notices/display/new/All/All/1';
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
      //console.log("removed no_border")
      //console.log($("#page_numbers ul")[0]==undefined)
      $("#notice_list").removeClass("no_border");
      //console.log("entered list_notices : " + page_no);
      $('div#notice_list').empty();

      $("#additional").slideDown();

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
            var d = context.notice.datetime_created.split('T')[0];
            d = Date.parse(d);
            if(d.getTime() == Date.parse("today").getTime())
              context["notice_date"] = "Today";
            else if(d.getTime() == Date.parse("yesterday").getTime())
              context["notice_date"] = "Yesterday";
            else if(d.getYear() == Date.parse("today").getYear())
              context["notice_date"] = d.toString('dd MMM');
            else
              context["notice_date"] = d.toString('dd MMM yyyy');

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

            //console.log("there you go")
            //console.log(context)
            $('#notice_list').append(list_notices_html(context));

      }
      $(".notice_date").each(function() {
              $(this).text($(this).text().substr(0,10));
              });
      //console.log("reh gya bhai")
      if($("#page_numbers ul")[0]==undefined)
          load_numbers_bar(ttotal_pages,sub_mode + "_");
}

function display_notice(id)
{
  read_notice(id);
  $.ajax({
    type: 'get',
    url : 'notices/get_notice/' + id + '/',
    success: function(data)
    {
      $('#content').append(display_notice_html(data));
      var count=0;
      for(var i=0;i<$('#_content img').length;i++)
      {
        var len1 = $('#_content img')[i].src.split('/').length;
        for(var j=0;j<$('#_content a').length;j++)
        {
          var len2 = $('#_content a')[j].href.split('/').length;
          //console.log("here");
          if($('#_content img')[i].src.split('/')[len1-1].split('.png')[0] == $('#_content a')[j].href.split('/')[len2-1].split('.pdf')[0])
            {
              //console.log("there");
              //console.log($('#_content a')[j].href);
              href1 = $('#_content a')[j].href.replace(window.location.origin,'').replace(/\%20/g, ' ');
              $('#_content a')[j].a;
              $('a[href="' + href1 + '"]').replaceWith('<div class="button4 button-div" onclick="window.location=\''+ href1 +'\'">Download pdf</div>');
            }
        }
      }

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
      //console.log("entered search");
      if($("#search-inp").val()!=search_string)
        search_string_changed=1;
      search_string = $("#search-inp").val();
      search_change_page(1);
}

function check_if_date()
{
      //console.log("entered check_if_date");
      url="";
      if(search_string.split("to ").length==2)
      {
        //console.log("entered check_ifdate");
        parts=search_string.split("to ");

        parts[0]=parts[0].replace( /(\d{2})\/(\d{2})\/(\d{4})/, "$2/$1/$3");      //Conversion of MM-DD-YYYY to DD-MM-YYYY
        parts[0]=parts[0].replace( /(\d{2})-(\d{2})-(\d{4})/, "$2/$1/$3");
        parts[1]=parts[1].replace( /(\d{2})\/(\d{2})\/(\d{4})/, "$2/$1/$3");
        parts[1]=parts[1].replace( /(\d{2})-(\d{2})-(\d{4})/, "$2/$1/$3");

        parts[0]=Date.parse(parts[0]).getTime();
        parts[1]=Date.parse(parts[1]).add(1).days().getTime();
        //console.log(parts[1]);
//        if(parts[0]>1262284200000 && parts[1]>1262284200000)
        url = ">>" + parts.join().replace(",", "-");
        //console.log("url : ", url);
      }
      else if(!isNaN(Date.parse(search_string)) && Date.parse(search_string)>1262284200000 && Date.parse(search_string)<2531673000000)
      {
        var temp = search_string;
        temp=temp.replace( /(\d{2})\/(\d{2})\/(\d{4})/, "$2/$1/$3");      //Conversion of MM-DD-YYYY to DD-MM-YYYY
        temp=temp.replace( /(\d{2})-(\d{2})-(\d{4})/, "$2/$1/$3");
        x = Date.parse(temp);
        url = ">>" + x.getTime() + "-" + x.add(1).days().getTime();
      }
      //console.log("url : " + url);
      return url;
}

function bring_search_url()
{
      url = check_if_date();
      if(url==="")
      {
          if(search_string==="")
            return "";
          query=search_string.split(" ");
          t=0;
          k=query.length;
          for(var i=0; i<k;i++)
          {
            if(query[t]==="")
              query.splice(t,1);
            else
              t++;
          }
          for(var k=0; k<query.length-1; k++)
          {
            url+=query[k]+"+";
          }
          url+=query[query.length-1];
      }
      return url;
}

function bring_search_results()
{
      url = bring_search_url();
      //console.log(url);
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
            //console.log("search_done");
            //console.log(search_store);
            //console.log("search_ends");
            store_to_use = search_store;
            load_numbers_bar(search_total_pages, "search_");
            if(search_total_pages!==0)
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

        url = 'notices/read_star_notice/'+id+'/'+'remove_starred/';
        delete check_star_array[id];
          $("#star_shape_" + id).attr({style : "color:#AAA"});
      }
      else
      {
        url = 'notices/read_star_notice/'+id+'/'+'add_starred/';

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
      nucleus.setShowLoadingOff();
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
		url = 'notices/read_star_notice/'+id+'/'+'add_read/';
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
  if(r===true)
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
  //console.log("gaind7");
  var x = document.getElementById("check-" + id).checked;
  if(!x)
    delete checklist[id];
  else
    checklist[id]=1;
  if(Object.keys(checklist).length===0)
  {
    $('#more').unbind("click", show_menu);
    $('#more').bind("click", bind_unbind_tooltip);
    binding_done=0;
  }
  else
  {
    if(binding_done===0)
    {
      $('#more').unbind("click", bind_unbind_tooltip);
      $('#more').bind("click", show_menu);
      binding_done=1;
    }
  }
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

    if(parseInt(cur_page_no)<window[mode_prefix + "_total_pages"]||window[mode_prefix + "_last_page_notices"]===0)
      k=10;
    else
      k=window[mode_prefix + "_last_page_notices"];
    //console.log(x);
    if(x)
    {
        //console.log("11");
        $('.checkboxes').prop('checked', true);
        if(binding_done==0)
        {
          $('#more').unbind("click", bind_unbind_tooltip);
          $('#more').bind("click", show_menu);
          binding_done=1;
        }
        for(var i=0; i<k; i++)
        {
            id = $('.checkboxes')[i].id.substr(6);
            checklist[parseInt(id)]=1;
        }
    }
    else
    {
        //console.log("22");
        $('.checkboxes').prop('checked', false);
        for(var i=0; i<k; i++)
        {
            id = $('.checkboxes')[i].id[6]+$('.checkboxes')[i].id[7];
            delete checklist[parseInt(id)];
        }
        if(Object.keys(checklist).length===0)
        {
          $('#more').unbind("click", show_menu);
          $('#more').bind("click", bind_unbind_tooltip);
          binding_done=0;
        }
    }
}

function show_menu(e)
{
    //console.log(e);
    //console.log("below e");
    if(more==1)
    {
      $("#super_more").empty();
      more=0;
    }
    else
    {
        $('#super_more').append(more_html());
        more=1;
    }
    if(e.stopPropagation)
        e.stopPropagation();
    else
        e.cancelBubble = true;
}

function insert_and_maintain_datesort(notice)
{
  //console.log(notice);
   len = starred_array.length;
     if(len===0)
       starred_array.push(notice);
     else if(len==1)
     {
         if(notice.datetime_created>=starred_array[0].datetime_created)
          starred_array.splice(0, 0, notice);
         else
          starred_array.splice(1, 0, notice);
     }  
     else
     {
       if(notice.datetime_created>=starred_array[0].datetime_created)
        starred_array.splice(0, 0, notice);
       else if(notice.datetime_created<=starred_array[len-1].datetime_created)
        starred_array.splice(len, 0, notice);
       else
       {
         for(var i=1;i<len;i++)
           if(notice.datetime_created<=starred_array[i-1].datetime_created && notice.datetime_created>=starred_array[i].datetime_created)
           {
             starred_array.splice(i, 0, notice);
             break;
           }
       }
     }
}

function read_star_checklist(t)
{
    $("#super_more").empty();
    more=0;
    //console.log("entered read_star_checklist t :" + t);
    a = Object.keys(checklist);
    //console.log(a);
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
        $("#star_shape_" + a[i]).attr({style : "color:#F1C40F"});
      }
      else if(t==2)
      {
        //console.log(a[i]);
        if(check_star_array[a[i]]===undefined)
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
        $(".notice_date").attr({class : "notice_date read"});
        $(".notice_source").attr({class : "notice_source read"});
        $(".notice_subject").attr({class : "notice_subject read"});
      }
      else
      {
        delete read_array[a[i]];
        $("#notice_"+a[i]).attr({class : "notice_info unread"});
        $(".notice_date").attr({class : "notice_date unread"});
        $(".notice_source").attr({class : "notice_source unread"});
        $(".notice_subject").attr({class : "notice_subject unread"});
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
    nucleus.setShowLoadingOff();
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

function display_categories(e)
{
  $("#super_more").empty();
  more=0;
  //console.log("hello");
  //console.log(e);
  if(select_category===0)
  {
    $('#select_bars').addClass("select_bars_clicked");
    $('#button_category_app_name').append(display_categories_html());
    select_category=1;
  }
  else
  {
    $('#select_bars').removeClass("select_bars_clicked");
    $('#category_menu').remove();
    select_category=0;
  }
  if(e.stopPropagation)
      e.stopPropagation();
  else
      e.cancelBubble = true;
}

function display_sub_categories(main_category, e)
{
  var len=constants[main_category].length;
  var k=Math.min(len, 11);
  $('#category_details').empty(); $('#category_child2').empty();
  if(len!==0)
  {
    $('#category_details').append('<div id="category_child1"></div><div id="category_child2"></div>');
    $('#category_child1').append(display_sub_categories_html(0, k, main_category));
    $('#category_child2').append(display_sub_categories_html(k, len, main_category));
  }
  else
    $('#category_details').append('<div class="no_sub_categories">No sub-categories</div>');
}

$('html').click(function(){
      $("#super_more").empty();
      more=0;
      $('#select_bars').removeClass("select_bars_clicked");
      $('#category_menu').remove();
      select_category=0;
});

$('#category_menu').click(function(e){
  if(e.stopPropagation)
      e.stopPropagation();
  else
      e.cancelBubble = true;
});

$('#super_more').click(function(e){
  if(e.stopPropagation)
      e.stopPropagation();
  else
      e.cancelBubble = true;
});

function change_category_bar_name(main_category, category)
{
    //console.log("entered change_category_bar_name");
    $('#category_menu').remove();
    select_category=0;
    $('#select_bars').removeClass("select_bars_clicked");
    if(m_category==main_category && sub_category==category)
      return;
    url_temp = '#notices/' + main_mode + '/' + sub_mode + '/' + main_category +'/' +  category + '/1';
    location.hash = url_temp;
}

function newold_clicked(ns)       //ns stands for new status, storing the sub_mode of the button that is clicked.
{
    //console.log("entered newold_clicked");
    if(sub_mode!=ns)
    {
      url_temp = '#notices/' + main_mode + '/' + ns + '/' + m_category +'/' +  sub_category + '/1';
      location.hash = url_temp;
    }
}

function evaluate_breadcrumbs()
{
    var notice_prefix;
      //console.log("1abcasd");
    if(main_mode=="content")
    {
      //console.log("abcasd");
      temp_arr = prev_content_url.split("/");
      main_mod=temp_arr[1];
      sub_mod=temp_arr[2];
      m_categor=temp_arr[3];
      sub_categor=temp_arr[4];
    }
    else
    {
      main_mod=main_mode;
      sub_mod=sub_mode;
      m_categor=m_category;
      sub_categor=sub_category;
    }
    if(sub_mod=="new")
      notice_prefix = "Current"
    if(sub_mod=="old")
      notice_prefix = "Expired"

    if(main_mod=="display")
    {
      if(all==1)
      create_breadcrumbs(notice_prefix + "Notices", "All", 1);
      else
      create_breadcrumbs(notice_prefix + "Notices", m_categor, sub_categor, 1);
    }
    else if(main_mod=="search")
    {
      if(all==1)
        create_breadcrumbs("SearchedNotices", notice_prefix, "All", 0);
      else
        create_breadcrumbs("SearchedNotices", notice_prefix, m_categor, sub_categor, 0);
    }
}

function create_breadcrumbs()
{
  //console.log("entered : create_breadcrumbs");
  //console.log(arguments[0] + arguments[1] + arguments[2]);
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
  //console.log(tag_type);
  if(main_mode=="content")
  {
    //console.log("abcasd");
    temp_arr = prev_content_url.split("/");
    main_mod=temp_arr[1];
    sub_mod=temp_arr[2];
    m_categor=temp_arr[3];
    sub_categor=temp_arr[4];
  }
  else
  {
    main_mod=main_mode;
    sub_mod=sub_mode;
    m_categor=m_category;
    sub_categor=sub_category;
  }
  url = "";
  if(tag_type==0)                                             //coded 0 : main_mode
    url = '#notices/' + main_mod + '/new/All/All/1'
  if(tag_type==1)                                              //coded 1 : sub_mode
    url = '#notices/' + main_mod + '/' + sub_mod + '/All/All/1'
  if(tag_type==2)                                            //coded 2 : m_category
    url = '#notices/' + main_mod + '/' + sub_mod + '/' + m_categor + '/All/1'
  if(tag_type!=3)
  location.hash = url;
}

function prev_next_clicked(state)                                         //Previous or next buttons clicked in content mode
{
  //console.log("prev_next_clicked entered : " + state);
  //console.log("prev_content_url_begin" + prev_content_url);
  url_split = prev_content_url.split('/');
  leng = url_split.length;
  prev_page_no = url_split[leng-1];
  prev_mode = url_split[1];
  id = location.hash.split('/')[2];
  len = store_to_use.length;
  var i=0;
//  //console.log("bazooka" + state);

  if(prev_mode=="display")                  //Since temp_store is currently the only one managed in bundles, so different analysis than upload_array
  {
    for(i; i<len; i++)
    {
//      //console.log(i);
//      //console.log(id);
      if(store_to_use[i].id==id)
      {
//      //console.log(id);
          if(state===-1)
          {
            cur_page_no = Math.floor(i/10) + 1;
            return;
          }
          else if(state===0)
            cur_page_no = Math.floor((i-1)/10) + 1;
          else
            cur_page_no = Math.floor((i+1)/10) + 1;
//  //console.log("exception" + cur_page_no);
//      //console.log(i + "state : " + state + " page_no : " + cur_page_no );
          if(state===0 && store_to_use[i-1]!=undefined)
            location.hash = '#notices/content/' + store_to_use[i-1].id;
          else if(state===1 && store_to_use[i+1]!=undefined)
            location.hash = '#notices/content/' + store_to_use[i+1].id;
          else
          {
            content_button_state = state;
            gap_scanner();      //If on clicking next/prev the notice is not available, bring the entire bundle first
            return
          }
          break;
      }
    }
    url_split[leng-1] = cur_page_no;
    prev_content_url = url_split.join().replace(/,/g, '/');
//      //console.log(prev_content_url + "prev_content_url");
  }
  else
  {
    var i;
    if(state===0)
      i=1;
    else
      len=len-1;
    for(i; i<len; i++)
      if(store_to_use[i].id==id)
      {
          if(state===0)
          {
            cur_page_no = Math.floor((i-1)/10) + 1;
            location.hash = '#notices/content/' + store_to_use[i-1].id;
          }
          else
          {
            cur_page_no = Math.floor((i+1)/10) + 1;
            location.hash = '#notices/content/' + store_to_use[i+1].id;
          }
      }

    url_split[leng-1] = cur_page_no;
    prev_content_url = url_split.join().replace(/,/g, '/');
  }
}

function write_no_notices_yet()
{
  no_notices=1;
  //console.log("added no_border");
  $("#notice_list").empty();
  $("#notice_list").addClass("no_border");
  $("#notice_list").append("<div id='no_notices' class='no-events'>No Notices yet!</div>");
  $("#additional").slideUp();
}

function bind_unbind_tooltip()
{
    $('#more').tooltip({position: {at: "right+5 top-20"}});
    $('#more').tooltip("open");
    $('#more').mouseout(function(){setTimeout( function(){
                 if($("#more").data('ui-tooltip')!==undefined)
                    $('#more').tooltip("destroy");
                }, 500 );
        });
}

function search_keydown(event)
{
    if(event.which==13)
          {
                  //console.log("search_global_bar");
                  set_search_string();
          }
}


function stop_propagation(e)
{
    //console.log("entered stop_propagtion");
    if(e.stopPropagation)
        e.stopPropagation();
    else
        e.cancelBubble = true;
}

function open_upload_dialog()
{
    dialog_iframe({
      name:'notice_upload_dialog',
      title:'Upload a notice',
      width:1000,
      height:650,
      src:'/notices/upload',
  });

}

//Following are the functions that are called the first time, notices is clicked

function get_privelege()
{
      $.ajax({
        type: 'get',
        url : 'notices/privelege/',
        success: function (data)
        {
            if(data.privelege)
            {
              star_perm=1;
              privelege=1;
              bring_uploads();                         //First time function 2, in case user is an uploader
            }
            else if(user.is_authenticated)
            {
              star_perm=1;
              bring_starred_notices();                   //First time function 2, in case user is logged in and not an uploader
              //console.log("loaded get_privelge : privelege: " + privelege + " star_perm : " + star_perm)
            }
            else
            {
              get_total_notices_no_first_time();          //First time function 2, in case of anonymous user
              //console.log("loaded get_privelge : anonymous")
            }
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
              //console.log("loaded : total_notices_no old and new");
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
          for(var i=0; i<data['order'].length; i++)
          {
            constants[data['order'][i]] = data[data['order'][i]];
          }
          //console.log(data);
          //console.log("loaded : get_constants");
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
    //console.log("loaded : starred_notices");
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
    //console.log("loaded : read_notices");
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
           var dateA=new Date(a.datetime_created), dateB=new Date(b.datetime_created);
            return dateB-dateA; //sort by date descending
        })
        //console.log("loaded : bring_uploads");
        bring_starred_notices();              //First time function 3, in case user is an uploader
      }
   });
}

function gap_filler_first_time(bring_what)
{

        if(bring_what=="new")
          url = 'notices/list_notices/new/All/All/0/49/0/';
        else if(bring_what=="old")
          url = 'notices/list_notices/old/All/All/0/49/0/';
        else
          url = 'notices/list_notices/' + sub_mode + '/' + m_category + '/' + sub_category + '/0/49/0/';

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
           //console.log("loaded : gap_filler_first_time : " + bring_what);

           if(bring_what=="temp" && first_time_visit==1)
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
               first_time_visit=1;
               redirection();
             }
             else
               bring_content_first_time_notices();        //If the mode is content, bring 50 notices corresponding to id
           }
        }
        });
}
 
function bring_content_first_time_notices()               //If the mode is content, bring 50 notices corresponding to id
{
        id = location.hash.split('/')[2];
        //console.log("entered bring_content_first_time_notices");
        $.ajax({
        type: 'get',
        url : 'notices/content_first_time_notices1/' + id + '/',
        success: function (data)
        {
            $.ajax({
            type: 'get',
            url : 'notices/content_first_time_notices2/',
            success: function (set1)
            {
              var begin = set1["begin"];
              var end = set1["end"];
              var mode1 = set1["mode"];
              var page_no1 = set1["page_no"];
              if(mode1 == "new")
              {
                for(var i=0; i<data.length; i++)
                {
                  store[begin+i]=data[i];
                }
                temp_store = store;
              }
              else
              {
                for(var i=0; i<data.length; i++)
                {
                  old_store[begin+i]=data[i];
                }
                temp_store = old_store;
              }
              store_to_use = temp_store;
              first_time_visit=1;
              prev_content_url="#notices/display/" + mode1 + "/All/All/" + page_no1;
              redirection();
            }
            });
        }
        });
}

//Following are the functions which bring html from .hbs files

function welcome_html()
{
      return Handlebars.notices_templates.welcome({star_perm : star_perm});
}

function upload_html()
{
    return Handlebars.notices_templates.upload();
}

function load_cat_bar_html(name)
{
    //console.log("name : " + name + sub_category)
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

function prev_next_buttons_html()
{
    return Handlebars.notices_templates.prev_next_buttons();
}

function load_numbers_bar_html(tp23, mode1)
{
    numbers = [];
    for(var i=1;i<tp23;i++)numbers.push(i);
    return Handlebars.notices_templates.load_numbers_bar({ tp : tp23 , numbers : numbers, mode1 : mode1});
}

function display_notice_html(data)
{
    //console.log(data);
    data['datetime_created']=data['datetime_created'].replace("T", " ")
    var ref_exist = 0;
    if(data.reference!="")
      ref_exist = 1;
    return Handlebars.notices_templates.display_notice({data : data, ref_exist : ref_exist});
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
    html='';
    for(var i=initi;i<finali;i++)
    {
	html+='<div id=' + main_category + '_' + i + ' class="sub_categories" onclick="change_category_bar_name(\'' + main_category + '\', \'' + sub_categories[i] + '\')">' + sub_categories[i] + '</div>';
    }
    return html;
}

function list_notices_html()
{
    return Handlebars.notices_templates.list_notices(context);
}

function search_bar_html()
{
    return Handlebars.notices_templates.search_bar();
}

function create_breadcrumb_html(tag, code)
{
    return Handlebars.notices_templates.create_breadcrumb({tag : tag, code : code});
}
