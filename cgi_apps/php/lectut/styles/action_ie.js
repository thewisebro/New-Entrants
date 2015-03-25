function load()
{
	
	
	
	$('.scrollbarer').tinyscrollbar();
	
	if($('#main_goto').length>0)
	ie_func1('#main_goto');
	if($('#container').length>0)
	$('#container').css('height',$('body').height());

	$('#container').css('height',$('body').height());
	if($('#browse_by_department').length>0)
	$('#browse_by_department').css('top',-$('#container').height());
	//if($('#my_courses_page_container').length>0)
	//$('#my_courses_page_container').css('top',-$('#my_courses_goto').height());
	if($('#browse_by_department').length>0)
	{
		$('#browse_by_department_main_link').css('padding-top',($(window).height()+125-104-125-10)/2);
		$('#browse_by_department_mc_back').css('padding-bottom',($(window).height()-125-104-125-10)/2);
		$('#browse_by_department_mc_back_dummy').css('padding-top',($(window).height()-125-100-125)/2);
		
		
	}
	if($('#my_courses').length>0)
	{
		$('#my_courses_back').css('padding-top',($(window).height()+125-104-12-125-10)/2);
		$('#my_courses_bbd_back').css('padding-bottom',($(window).height()-125-104-125-10)/2);
		
	}
	if($('#search_play_area').length>0)
	{
	
		$('#back_link_container_mc').css('height',$(window).height());
		$('#my_courses_back').css('padding-top',($(window).height()+125-104-12-125)/2);
		$('#my_courses_bbd_back').css('padding-bottom',($(window).height()-125-104-125)/2);


	}
	
	if($('.link_space').length>0)
	$('.link_space').height($('#my_course_back').height());
	if($('#spacer').length>0)	
	$('#spacer').height($('#container').height());
	
	
	
	document.forms['login_form'].fakepassword.style.display = 'block';
	document.forms['login_form'].password.style.display = 'none';
	return;
	if($('#go_back_check').length>0)
		go_back();
	if($('#my_courses_course_selection').length>0)
	$('#my_courses_course_selection').tinyscrollbar();
	if($('#dummy_show_form').length>0)
		show_form();
	
	
	
	
}

function ie_func1(x)
{
$('.ss').addClass('hider');
$('.ss').removeClass('unhider');
$(x).removeClass('hider');
$(x).addClass('unhider');


}
function func1(x)
{

$('#container').stop().scrollTo(x,1500);

w=x;
setTimeout('go_back()', 1500);
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
		//alert("Please enter username and password.");
		$("#warning").html('Please enter username and password.');
		return false;
	}
	return true;
}

var k='#ec101';
var w='#main_goto';
var n="#ec102";

$(window).resize(function() {	
	
	$('#container').css('height',$(window).height());
	$('#container').css('height',$(window).height());
	$('#browse_by_department').css('top',-$('#container').height());
	$('#browse_by_department_main_link').css('padding-top',($(window).height()+125-104)/2);
	$('#browse_by_department_mc_back').css('padding-top',($(window).height()-125-104)/2);
	$('#browse_by_department_mc_back_dummy').css('padding-top',($(window).height()-125-100)/2);
	$('#my_courses_back').css('padding-top',($(window).height()+125-104)/2);
	$('#my_courses_bbd_back').css('padding-top',($(window).height()-125-104)/2);
	$('.link_space').height($('#my_course_back').height());
	$('#spacer').height($('#container').height());
	$('#container').stop().scrollTo(w,0);


});


	


function func1(x)
{

$('#container').stop().scrollTo(x,1500);

w=x;
setTimeout('go_back()', 1500);
}

function func2(x,y,z)
{


var t;
t=k+x;

$(y).stop().scrollTo(t,1500);
$('.my_courses_link').removeClass('my_courses_selected_link');
$('.my_courses_link').addClass('my_courses_inactive_link');


$(z).removeClass('my_courses_inactive_link');
$(z).addClass('my_courses_selected_link');




}

function func2_search(x,y,z)
{


var t;
t=k+x;
$(y).stop().scrollTo(x,1500);
$('.search_link').removeClass('search_selected_link');
$('.search_link').addClass('search_inactive_link');


$(z).removeClass('search_inactive_link');
$(z).addClass('search_selected_link');




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

showLTES(x,fac_id,fac_name,type);

n='#'+x;
$('.file').addClass('list_selected');
/*
$('.file').addClass('list_inactive');


$(z).removeClass('list_inactive');
$(z).addClass('list_selected');
*/

$('.bbd_course_link').removeClass('browse_by_department_course_link_selected');
$('.bbd_course_link').addClass('browse_by_department_course_link');

var t;
t=z+'_link';
$(t).removeClass('browse_by_department_course_link');
$(t).addClass('browse_by_department_course_link_selected');
k="#"+x;

}
function tu()
{
$('.scrollbarer').tinyscrollbar_update();
}
function func321(x,y,z)
{

showRegLTES(x);
n='#'+x;

$('.file').removeClass('list_selected');
$('.file').addClass('list_inactive');


$(z).removeClass('list_inactive');
$(z).addClass('list_selected');

func22('_lectures',y,'#browse_by_department_lectures_link');

$('.bbd_course_link').removeClass('browse_by_department_course_link_selected');
$('.bbd_course_link').addClass('browse_by_department_course_link')

var t;
t=z+'_link';
$(t).removeClass('browse_by_department_course_link');
$(t).addClass('browse_by_department_course_link_selected');


k="#"+x;

}


function func22(x,y,z)
{
var t;
t=n+x;
$('#browse_by_department_files').stop().scrollTo(t,1500);
$('.browse_by_department_link').removeClass('browse_by_department_selected_link');
$('.browse_by_department_link').addClass('browse_by_department_inactive_link');
$(z).removeClass('browse_by_department_inactive_link');
$(z).addClass('browse_by_department_selected_link');
}


function dept_goto(t,profList,depCode)
{

showProf(profList,depCode);
$('#details_tab_container').stop().scrollTo(t,1500);

}
function prof_goto(t,fac_id,fac_name)
{

showCourses(fac_id,fac_name);
$('#scroll_dept_target').stop().scrollTo(t,1500);
$('#scroll_prof_target').stop().scrollTo('#browse_by_department_files',1500);
$('.profs_dept').removeClass('prof_active');
$('.profs_dept').addClass('prof_inactive');
$('#prof_container').addClass('prof_inactive');

$('#go_back').css('color','#00a0b0');


}

function f()
{
$('#details_tab_container').stop().scrollTo('#ec102_lectures',1500);$('.profs_dept').addClass('prof_active');
$('.profs_dept').removeClass('prof_inactive');
$('#prof_container').removeClass('prof_inactive');
$('.file_list').text(' ');
$('#browse_by_department_course_selection').text(' ');$('.profs_dept').addClass('prof_active');
$('.profs_dept').removeClass('prof_inactive');
$('#prof_container').removeClass('prof_inactive');
$('.file_list').text(' ');
$('#browse_by_department_course_selection').text(' ');

$('#scroll_dept_target').stop().scrollTo('#dept_list',500);
$('#scroll_prof_target').stop().scrollTo('#profs_container',1500);
$('#go_back').css('color','white');

$('#scroll_dept_target').stop().scrollTo('#dept_list',500);$('.profs_dept').addClass('prof_active');
$('.profs_dept').removeClass('prof_inactive');
$('#prof_container').removeClass('prof_inactive');
$('.file_list').text(' ');
$('#browse_by_department_course_selection').text(' ');

$('#scroll_dept_target').stop().scrollTo('#dept_list',500);
$('#scroll_prof_target').stop().scrollTo('#profs_container',1500);
$('#go_back').css('color','white');
$('#scroll_prof_target').stop().scrollTo('#profs_container',1500);
$('#go_back').css('color','white');

}

function go_back()
{
$('.profs_dept').addClass('prof_active');
$('.profs_dept').removeClass('prof_inactive');
$('#prof_container').removeClass('prof_inactive');
$('.file_list').text(' ');
$('#browse_by_department_course_selection').text(' ');

$('#scroll_dept_target').stop().scrollTo('#dept_list',500);
$('#scroll_prof_target').stop().scrollTo('#profs_container',1500);
$('#go_back').css('color','white');
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
