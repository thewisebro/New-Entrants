function loadResult(form)
{
	if (window.XMLHttpRequest)                                                          
	{// code for IE7+, Firefox, Chrome, Opera, Safari                                   
		xmlhttp=new XMLHttpRequest();                                                   
	}
	else                                                                                
	{// code for IE6, IE5                                                               
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}

	document.getElementById('advanced').style.display = 'none';
	document.getElementById('adv_right').className='advUp';
	var str="Name="+form.Name.value+"&form_submitted=true&search_category="+active+"&student_programme="+form.student_programme.value+"&student_year="+form.student_year.value+"&student_deptt="+form.student_deptt.value+"&faculty_deptt="+form.faculty_deptt.value+"&services_list="+form.services_list.value+"&faculty_post="+form.faculty_post.value+"&advanced_search_status="+form.advanced_search_status.value;                                  
	xmlhttp.open("GET","ajaxresult.cgi?"+str,false);                                    
	xmlhttp.send();
	document.getElementById("results").innerHTML=xmlhttp.responseText;                  
	form.advanced_search_status.value = "off";                                          
	return false;                                                                       
}
var active='all';
var advanced_search_status="off";                                                       
function switchSearch(tab)                                                              
{
	if(active!=tab)                                                                     
	{
		document.getElementById(active+'_tab').className='inactive_tab';
		document.getElementById('img_'+active+'_left').className='inactive_left';
		document.getElementById('img_'+active+'_right').className='inactive_right';     
		if(tab!='all')                                                                  
		{
			document.getElementById(active).style.display="none";                       
			active=tab;
			document.getElementsByTagName("form")[0].search_category.value=active;
			document.getElementById('advanced_main').style.display = 'block';
		}
		else
		{
			document.getElementById(active).style.display="none";
			active='all';
			document.getElementsByTagName("form")[0].search_category.value=active;
			document.getElementById('advanced_main').style.display = 'none';

		}
		document.getElementById(active).style.display="block";
		document.getElementById(active+'_tab').className='active_tab';
		document.getElementById('img_'+active+'_left').className='active_left';
		document.getElementById('img_'+active+'_right').className='active_right';
	}
}


function advDrop()
{
	if(active == "all")
		return;
	if(document.getElementById('adv_right').className=='advUp')
	{
		document.getElementById('advanced').style.display = 'block';
		document.getElementById('adv_right').className='advDown';
		document.getElementsByTagName("form")[0].advanced_search_status.value="on";
	}
	else
	{
		document.getElementById('advanced').style.display = 'none';
		document.getElementsByTagName("form")[0].advanced_search_status.value="off";
		document.getElementById('adv_right').className='advUp';
	}
}

