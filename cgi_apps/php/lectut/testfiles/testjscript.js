function GetXmlHttpObject()
{
	var xmlhttp;
	if (window.XMLHttpRequest)
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}
	else
	// code for IE6, IE5
	xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	return xmlhttp;
}
/*
function showHint(str)
{
	if (str.length==0)
	{
	document.getElementById("txtHint").innerHTML="";
	return;
	}
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
			alert("ready");
			document.getElementById("txtHint").innerHTML=xmlhttp.responseText;
		}
	}
	xmlhttp.open("GET","/lectut/common/gethint.php?q="+str,true);
	xmlhttp.send();
}
*/
function uploadAjax(form)
{
	document.getElementById("addAnotherFile").style.display='';
	var send="fac_id="+form.fac_id.value+"&type="+form.type.value+"&subcode="+form.subcode.value+"&file="+form.file.value+"&permission="+form.permission.value+"&year="+form.year.value+"&link="+form.link.value;
	
	xmlhttp=GetXmlHttpObject();
	if(xmlhttp==null)
	{
		alert("Browser does not support HTTP Request");
		return;
	}

	xmlhttp.open("POST","/lectut/pages/uploadlec.php",true);
	
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
}

function show_form()
{
	document.getElementById("uploadFormMain").style.display='';
	document.getElementById("show_exam_year").style.display='none';
	document.getElementById("show_soln_link").style.display='none';
	document.getElementById("addAnotherFile").style.display='none';
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

