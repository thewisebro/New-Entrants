//global variables used
var k='#ec101';
var w='#main_goto';
var n="#ec102";
var input_focused = 0;
var open_facebox = 'dummy';
var i=false;

function func1(x)
{

if($.browser.msie && $.browser.version.slice(0,3) =="7.0")
{
$('.ss').css('display','none');
$(x).css('display','block');
if(x=='#my_courses_goto')
s();
}

$('#container').stop().scrollTo(x,800);

w=x;
if($('#go_back').length>0)

$('#container').stop().scrollTo(x,800);

w=x;
if($('#go_back').length>0)
setTimeout('go_back()', 800);
}

function func2(x,y,z)
{


var t;
t=k+x;

$(y).stop().scrollTo(t,800);
$('.my_courses_link').removeClass('my_courses_selected_link');
$('.my_courses_link').addClass('my_courses_inactive_link');


$(z).removeClass('my_courses_inactive_link');
$(z).addClass('my_courses_selected_link');


if(!($.browser.msie))
{
if($('#scrollbarer .overview').length>0)
{$('#scrollbarer .overview').css('height',$(t).height());$("#scrollbarer").tinyscrollbar_update();}
}

}

function func2_search(x,y,z)
{


var t;
t=k+x;
$(y).stop().scrollTo(x,800);
$('.search_link').removeClass('search_selected_link');
$('.search_link').addClass('search_inactive_link');


$(z).removeClass('search_inactive_link');
$(z).addClass('search_selected_link');

if(!($.browser.msie))
{
if($('.scrollbarer .overview').length>0)
{ $('.scrollbarer .overview').css('height',$(x).height()); $('.scrollbarer').tinyscrollbar_update();}
}


}

function func3(x,y,z)
{



k='#'+x;
$('.file').removeClass('list_selected');
$('.file').addClass('list_inactive');


$(z).removeClass('list_inactive');
$(z).addClass('list_selected');
func2('_lectures','#my_courses_files','#my_courses_lectures_link');

$('.mc_course_link').removeClass('my_courses_course_link_selected');
$('.mc_course_link').addClass('my_courses_course_link')

var t;
t=z+'_link';
$(t).removeClass('my_courses_course_link');
$(t).addCla$('.scrollbarer').tinyscrollbar();
	$('#scrollbarer').tinyscrollbar();
ss('my_courses_course_link_selected');
}


function func32(x,y,z,fac_id,fac_name,type)
{

var i=true;
setTimeout("if(i==true)$('#subjects').text('Loading...')",0);
showLTES(x,fac_id,fac_name,type);
i=false;

n='#'+x;
$('.file').removeClass('list_selected');
$('.file').addClass('list_inactive');

$('.my_courses_course_link').removeClass('my_courses_course_link_selected');
$('.browse_by_department_course_link').removeClass('browse_by_department_course_link_selected');

$(z).removeClass('list_inactive');
$(z).addClass('list_selected');

//$('.bbd_course_link').removeClass('browse_by_department_course_link_selected');
//$('.bbd_course_link').addClass('browse_by_department_course_link');

if(type == 'del')
{

  func2('_lectures','#browse_by_dpartment_files','#browse_by_department_lectures_link');
  $(z+"_link").addClass('my_courses_course_link_selected');
}
else
{
  func22('_lectures','#browse_by_dpartment_files','#browse_by_department_lectures_link');

  $(z+'_link').addClass('browse_by_department_course_link_selected');
}
//var t;
//t=z+'_link';
k="#"+x;

$('#scroll_prof_target').stop().scrollTo('#browse_by_department_files',800);
//func2('_lectures','#my_courses_files','#my_courses_lectures_link');
}



function tu()
{
$('.scrollbarer').tinyscrollbar_update();
}
function func321(x,y,z)
{
 
var i=true;
setTimeout("if(i==true)$('#subjects_reg').text('Loag...')",0);
showRegLTES(x);

i=false;

n='#'+x;

$('.file').removeClass('list_selected');
$('.file').addClass('list_inactive');

//var i=z + "_link";
$('.my_courses_course_link').removeClass('my_courses_course_link_selected');
//$(z + "_link").addClass('my_courses_course_link_selected');

$(z).removeClass('list_inactive');
$(z).addClass('list_selected');
//setTimeout("func2('_lectures','#my_courses_files','#my_courses_lectures_link')",500);
//$('.bbd_course_link').removeClass('browse_by_department_course_link_selected');
//$('.bbd_course_link').addClass('browse_by_department_course_link');

//var t;
//t=z+'_link';
//$(t).removeClass('browse_by_department_course_link');
//$(t).addClass('browse_by_department_course_link_selected');


k="#"+x;

}


function func22(x,y,z)
{
var t;
t=n+x;
$('#browse_by_department_files').stop().scrollTo(t,800);
$('.browse_by_department_link').removeClass('browse_by_department_selected_link');
$('.browse_by_department_link').addClass('browse_by_department_inactive_link');
$(z).removeClass('browse_by_department_inactive_link');
$(z).addClass('browse_by_department_selected_link');
if(!($.browser.msie))
{
if($('.scrollbarer').length>0)
{$('#browse_by_department .scrollbarer .overview').css('height',$(t).height()); $('#details_tab_container .scrollbarer').tinyscrollbar_update();}
}
}


function dept_goto(t,profList,depCode)
{
var i=true;
setTimeout("if(i==true)$('#profs').text('Loading...')",0);
showProf(profList,depCode);
i=false;
$('#details_tab_container').stop().scrollTo(t,800);
}

function prof_goto(t,fac_id,fac_name)
{

showCourses(fac_id,fac_name);
$('#scroll_dept_target').stop().scrollTo(t,800);
$('#scroll_dept_target .overview').css('top',0);
if(!$.browser.msie)
$('.scrollbarer').tinyscrollbar_update();

$('#scroll_prof_target').stop().scrollTo('#browse_by_department_files',800);
$('.profs_dept').removeClass('prof_active');
$('.profs_dept').addClass('prof_inactive');
$('#prof_container').addClass('prof_inactive');

$('#go_back').css('color','#00a0b0');


}

function f()
{
$('#details_tab_container').stop().scrollTo('#ec102_lectures',800);$('.profs_dept').addClass('prof_active');
$('.profs_dept').removeClass('prof_inactive');
$('#prof_container').removeClass('prof_inactive');
$('.file_list').text(' ');
$('#browse_by_department_course_selection').text(' ');$('.profs_dept').addClass('prof_active');
$('.profs_dept').removeClass('prof_inactive');
$('#prof_container').removeClass('prof_inactive');
$('.file_list').text(' ');
$('#browse_by_department_course_selection').text(' ');

$('#scroll_dept_target').stop().scrollTo('#dept_list',500);
$('#scroll_prof_target').stop().scrollTo('#profs_container',800);
$('#go_back').css('color','white');

$('#scroll_dept_target').stop().scrollTo('#dept_list',500);$('.profs_dept').addClass('prof_active');
$('.profs_dept').removeClass('prof_inactive');
$('#prof_container').removeClass('prof_inactive');
$('.file_list').text(' ');
$('#browse_by_department_course_selection').text(' ');

$('#scroll_dept_target').stop().scrollTo('#dept_list',500);
$('#scroll_prof_target').stop().scrollTo('#profs_container',800);
$('#go_back').css('color','white');
$('#scroll_prof_target').stop().scrollTo('#profs_container',800);
$('#go_back').css('color','white');
}

function go_back()
{
$('.profs_dept').addClass('prof_active');
$('.profs_dept').removeClass('prof_inactive');
$('#prof_container').removeClass('prof_inactive');
$('.file_list').text(' ');
$('#prof_name_bbd').text(' ');
$('#browse_by_department_course_selection').text(' ');
$('#scroll_dept_target').stop().scrollTo('#dept_list',500);
$('#scroll_prof_target').stop().scrollTo('#profs_container',800);
$('#go_back').css('color','white');
if($('#scroll_dept_target .overview').length>0)
$('#scroll_dept_target .overview').css('top',0);
if($('.scrollbarer').length>0)
$('.scrollbarer .overview').css('top',0,$('#prof_f_t').tinyscrollbar_update());
}



function getUrlVars()
{
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

function search_focus()
{
$('.search').addClass('search_focused');
$('.search').removeClass('search_unfocused');
}
function search_unfocus()
{
$('.search').removeClass('search_focused');
$('.search').addClass('search_unfocused');
}

function user_input_focus(x)
{
var u=document.getElementById(x);
if(document.forms['login_form'].username.value == 'Username')
document.forms['login_form'].username.value = '';
}

function user_input_unfocus(x)
{
var u=document.getElementById(x);
if(document.forms['login_form'].username.value == '')
document.forms['login_form'].username.value = 'Username';
}

function fake_focus()
{
document.forms['login_form'].fakepassword.style.display = 'none';
document.forms['login_form'].password.style.display = 'block';
document.forms['login_form'].password.focus();
}


function real_blur()
{
if(document.forms['login_form'].password.value == '')
{
	document.forms['login_form'].fakepassword.style.display = 'block';
	document.forms['login_form'].password.style.display = 'none';
}
}

function check_login()
{
	if(document.forms['login_form'].password.value == null || document.forms['login_form'].password.value == '' || document.forms['login_form'].username.value == null || document.forms['login_form'].username.value == '')
	{
		$("#warning").html('Please enter username and password.');
		return false;
	}
	return true;
}
function u()
{
$('#prof_f_t').tinyscrollbar_update();
}
function scroll_update()

{

$('#link_div .viewport').height($('#link_div .overview').height());
$('#link_div .viewport').height($('#link_div .overview').height());
if(!($.browser.msie))
$('.scrollbarer').tinyscrollbar_update();
}






//the code for keyboard controls begins here...


function keymanager(e){

var evtobj	=	window.event? event : e ;//distinguish between IE's explicit event object (window.event) and Firefox's implicit.

var unicode=evtobj.charCode? evtobj.charCode : evtobj.keyCode;

//var actualkey=String.toCharCode(unicode);
if (unicode==27 )
	{	
		if($('#meerkat-wrap').css('z-index')>0) $('.close-meerkat').trigger('click');
		$('#search_input').blur();
		facebox_close();		
	}


if (input_focused == 1) 
return;

if (unicode==188)
{
  if(evtobj.shiftKey)
  {
    if($('#go_back').length>0)
      go_back();
  }
}

if (unicode==83 )
	{	
		if($('#meerkat-wrap').length>0) $('.close-meerkat').trigger('click');
		else {
			s();
			if($.browser.msie)
			{			
				event.returnValue = false;
				setTimeout(function() { $("#search_input").focus(); }, 1000);	
			}			
			else
			{			
				e.preventDefault();
				$("#search_input").focus();
			}
			
			
		     }
	}
if (unicode == 39)
	{	
		if(w=="#main_goto") func1('#my_courses_goto');
		if(w=="#browse_by_department_goto") func1('#main_goto');	
	}
if (unicode == 37)
	{
		if(w=="#main_goto") func1('#browse_by_department_goto');
		if(w=="#my_courses_goto") func1('#main_goto');	
	}
if (unicode == 191)
	{
		
		
		if(evtobj.shiftKey)
		facebox_open('keyboard_shortcuts_facebox');	

	}


}
document.onkeydown=keymanager;



//fuctions for faceboxes
function facebox_open(x)
{
facebox_close();
document.getElementById("backy_fb").style.display="block";
document.getElementById(x).style.display="block";
open_facebox = x;
}

function facebox_close()
{

if($('#backy_fb').length==0 || open_facebox == "dummy")
return;
document.getElementById("backy_fb").style.display="none";
document.getElementById(open_facebox).style.display="none";

}


//asdaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

$(document).ready(function(){

//check for resize problems.....


	if($('#login_fresh_show').length>0)
	{
		facebox_open('login_fresh_show');
	}

	if(!($.browser.msie))
{
	$('.scrollbarer').tinyscrollbar();
	$('#prof_f_t').tinyscrollbar();
	$('#scrollbarer').tinyscrollbar();
	$('#my_courses_course_selection').tinyscrollbar();
}
	if($.browser.msie)
{
	$('.viewport').css('overflow-y','scroll');
	$('.scrollbar').css('display','none');
	
	if($.browser.version.slice(0,3)=="8.0")
	{
	$('.my_courses_back_link').css('top',0);
	$('.my_courses_bbd_back_link').css('top',0);
	}
	if($.browser.version.slice(0,3)=="7.0")
	{
	$('#browse_by_department').css('top',0);
	}
	
	
}
	$('#container').css('height',$(window).height());
	$('#browse_by_department').css('top',-$('#container').height());
        
	$("input").focus(function(){input_focused = 1;});
	$("input").blur(function(){input_focused = 0;});

	
	


	if($.browser.msie)
{
        $('.my_courses_back_link').css('margin-top',-320);
        $('.my_courses_bbd_back_link').css('margin-top',-200);
        $('#my_courses_bbd_back .my_courses_bbd_back_link').css('margin-top',-320);
	
}
	
	$('#browse_by_department_main_link').css('padding-top',($(window).height()+125-104)/2);
	$('#browse_by_department_mc_back').css('padding-top',($(window).height()-125-104)/2);
	$('#browse_by_department_mc_back_dummy').css('padding-top',($(window).height()-125-100)/2);
	$('#my_courses_back').css('padding-top',($(window).height()+125-104)/2);
	$('#my_courses_bbd_back').css('padding-top',($(window).height()-125-104)/2);
	$('.link_space').height($('#my_courses_back').height());
	$('#spacer').height($('#container').height());

	
	if($('#go_back_check').length>0)
		go_back();
	
	if($('#password_show').length>0)
	{
	document.forms['login_form'].fakepassword.style.display = 'block';
	document.forms['login_form'].password.style.display = 'none';
	document.forms['login_form'].fakepassword.blur();
	}

	
	if($('#upload').length>0)	
	show_form();
	
	if($.browser.msie)
	{
	s();
	}

	
	if(null != getUrlVars()["temp1"])
		{func1('#browse_by_department_goto');}
	else if(null != getUrlVars()["temp2"])
		func1('#my_courses_goto');
	else
		func1('#main_goto');

	if(!($.browser.msie))
	{
	if($(".scrollbarer").length>0)
		{setTimeout("$(\".scrollbarer\").tinyscrollbar_update()",500);}
	}

  if($('#warning_upload').length>0)
  {
     setTimeout("$('#warning_upload').text(' ')",2000);
  }
	
  if($('#warning_managefiles').length>0)
  {
     setTimeout("$('#warning_managefiles').text(' ')",2000);
  }

  if($(window).width()<=1024)
  {
    $("#my_courses").css("margin-left","0px");
    $("#my_courses").css("top","-100%");
  }
  else
  {
    $("#my_courses").css("margin-left","-512px");
    $("#my_courses").css("top","-125px");
  }

});







$(window).resize(function() {	
	
	$('#container').css('height',$(window).height());
	$('#browse_by_department').css('top',-$('#container').height());
	$('#browse_by_department_main_link').css('padding-top',($(window).height()+125-104)/2);
	$('#browse_by_department_mc_back').css('padding-top',($(window).height()-125-104)/2);
	$('#browse_by_department_mc_back_dummy').css('padding-top',($(window).height()-125-100)/2);
	$('#my_courses_back').css('padding-top',($(window).height()+125-104)/2);
	$('#my_courses_bbd_back').css('padding-top',($(window).height()-125-104)/2);
//	$('.link_space').height($('#my_course_back').height());
	$('#spacer').height($('#container').height());
	$('#container').stop().scrollTo(w,0);
  if($(window).width()<=1024)
  {
    $("#my_courses").css("margin-left","0px");
    $("#my_courses").css("top","-100%");
  }
  else
  {
    $("#my_courses").css("margin-left","-512px");
    $("#my_courses").css("top","-125px");
  }

});







