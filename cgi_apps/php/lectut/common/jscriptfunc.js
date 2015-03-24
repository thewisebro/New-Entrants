function hide_doyou()                      
{                       
     document.getElementById('doyou').style.display="none";                
}                                                                         
                                                                       
function show_doyou()                                                 
{                                                                         
     document.getElementById('doyou').style.display="inline";              
}
   
function validate_form()
{
if($('.chk:checked').length == 0 && $('.chk_all:checked').length == 0)
{
	alert("Please select a file.");
	return false;
}
return true;
}

var select_all_checker = true;

function select_all( id, pID )
{
   $( "#" + pID + " :checkbox").attr('checked', select_all_checker);
   if(select_all_checker == false)
   select_all_checker = true;
   else
   select_all_checker = false;
}

function validate_upload_form()
{
	var courseId=$("#subcodeId").val();
	var file=$("#uploadFile").val();
	var topic=$("#Topic").val();
	if(courseId==null || courseId=="")
	{
		alert("Please enter Course Id.");
		return false;
	}
	else if(file==null || file=="")
	{
		alert("Please select a file.");
		return false;
	}
	else if(topic==null || topic=="")
	{
		alert("Please enter Topic.");
		return false;
	}
	return true;	
}

function GetXmlHttpObject()
{
	var xmlhttp;
	if (window.XMLHttpRequest)
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}
	else
	{// code for IE6, IE5
		try
		{
			xmlhttp = new ActiveXObject("Msxml2.XMLHTTP.6.0");
		}
		catch (e)
		{
			try
			{
				xmlhttp = new ActiveXObject("Msxml2.XMLHTTP.3.0");
			}
			catch (e)
			{
				try
				{
					xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
				}
				catch (e)
				{
					alert("Browser does not support XMLHttpRequest.");
					return false;
				}
			}
		}
	}
	return xmlhttp;
}

function showUploaded(str,facId)
{
	if (str.length==0)
	{
	document.getElementById("show_uploaded").innerHTML="";
	scroll_update();
	return;
	}
	xmlhttp=GetXmlHttpObject();
	if(xmlhttp==null)
	{
		alert("Browser does not support HTTP Request");
		scroll_update();
		return;
	}
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			document.getElementById("show_uploaded").innerHTML=xmlhttp.responseText;
			scroll_update();

		}
    else
      showLoading("#show_uploaded","../styles/ajax-loader-blue.gif");
    

	}
	xmlhttp.open("GET","../pages/link_file.php?type="+str+"&subcode="+$('#subcodeId').val(),true);
  xmlhttp.send();
}

function showCourses(facId,Name)
{
	xmlhttp=GetXmlHttpObject();
	if(xmlhttp==null)
	{
		alert("Browser does not support HTTP Request");
		return;
	}
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			document.getElementById("browse_by_department_course_selection").innerHTML=xmlhttp.responseText;
      document.getElementById("prof_name_bbd").innerHTML=Name;
		}
    else
      showLoading("#browse_by_department_course_selection","../styles/ajax-loader-blue.gif");

	}
	xmlhttp.open("GET","../pages/course1.php?id="+facId+"&name="+Name,true);
	xmlhttp.send();
}

function showLTES(course,facId,Name,type)
{
	xmlhttp=GetXmlHttpObject();
	if(xmlhttp==null)
	{
		alert("Browser does not support HTTP Request");
		return;
	}
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			document.getElementById("subjects").innerHTML=xmlhttp.responseText;
			if(!($.browser.msie) && $('#prof_f_t').length>0)
			$('#prof_f_t').tinyscrollbar_update();
			if($('#my_courses').length>0)
			func2('_lectures','#my_courses_files','#my_courses_lectures_link');
			if($('#scrollbarer').length>0)
			$('#scrollbarer').tinyscrollbar_update();
			
		}
    else
    {
          if(type=='down')
          {showLoading("#subjects","../styles/ajax-loader-blue.gif");}
          else
          {showLoading("#subjects","../styles/ajax-loader-red.gif");}
    }

	}
	if(type=='down')
	{
		
		xmlhttp.open("GET","../pages/course2.php?course="+course+"&id="+facId+"&name="+Name,true);
	}
	else
	{
		xmlhttp.open("GET","../pages/course3.php?course="+course+"&id="+facId+"&name="+Name,true);
	}
	xmlhttp.send();
}

function showRegLTES(course)
{
	xmlhttp=GetXmlHttpObject();
	if(xmlhttp==null)
	{
		alert("Browser does not support HTTP Request");
		return;
	}
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			//document.getElementById("subjects_reg").innerHTML=xmlhttp.responseText;
			$('#subjects_reg').html(xmlhttp.responseText);
		//	if(!($.browser.msie))
        func2('_lectures','#my_courses_files','#my_courses_lectures_link')
//			$('#scrollbarer').tinyscrollbar_update();
}
else
showLoading("#subjects_reg","../styles/ajax-loader-red.gif");
	}
	xmlhttp.open("GET","../pages/reg_course.php?course="+course,true);
	xmlhttp.send();
}

function showProf(profList,depCode)
{
	xmlhttp=GetXmlHttpObject();
	if(xmlhttp==null)
	{
		alert("Browser does not support HTTP Request");
		return;
	}
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			document.getElementById("profs").innerHTML=xmlhttp.responseText;
      $("#details_tab_container .scrollbarer").tinyscrollbar_update();
		}
    else
         showLoading("#profs","../styles/ajax-loader-blue.gif");

	}
  
	xmlhttp.open("GET","../pages/prof_list.php?profList="+profList+"&depCode="+depCode,true);
	xmlhttp.send();
}

/*function uploadAjax(form)
{
	document.getElementById("addAnotherFile").style.display='';
	var send="fac_id="+form.fac_id.value+"&type="+form.type.value+"&subcode="+form.subcode.value+"&file="+form.file.value+"&permission="+form.permission.value+"&year="+form.year.value+"&link="+form.link.value;
	
	xmlhttp=GetXmlHttpObject();
	if(xmlhttp==null)
	{
		alert("Browser does not support HTTP Request");
		return;
	}

	xmlhttp.open("POST","../pages/uploadlec.php",true);
	
	xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	
	xmlhttp.setRequestHeader("Content-length", send.length);
	
	xmlhttp.setRequestHeader("Connection", "close");
	
	xmlhttp.onreadystatechange=function()
	{		
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			alert("hi");
			document.getElementById("resultUpload").innerHTML=xmlhttp.responseText;
		}
	}
	
	xmlhttp.send(send);
}*/

function show_form()
{
	document.getElementById("upload").style.display='';
	document.getElementById("show_exam_year").style.display='none';
	document.getElementById("show_soln_link").style.display='none';
}

function show_form_special(type)
{
	switch(type)
	{
		case 'exam':
			document.getElementById("show_exam_year").style.display='';
			document.getElementById("show_soln_link").style.display='none';
			break;

		case 'soln':
			document.getElementById("show_exam_year").style.display='none';
			document.getElementById("show_soln_link").style.display='';
			break;
		default :
			document.getElementById("show_exam_year").style.display='none';
			document.getElementById("show_soln_link").style.display='none';
			break;
	}


}
function showLoading(eId,image) {
  //alert(eId+" "+image);
  $(eId).html("<img src='"+image+"' />");
}
