function updateInfo(action,mode)
{
	switch(action)
	{
		case "ShowUsers":
				loadData('showUsers.php');
				break;
	
		case "ShowApprovedUsers":
				loadData('showApprovedUsers.php');
				break;
		case "ShowRejectedUsers":
				loadData('showRejectedUsers.php');
				break;
		case "ShowMarkedUsers":
				loadData('showMarkedUsers.php');
				break;
		case "ShowProblems":
				loadData('showProblems.php');
				break;
		case "ShowSuggestions":
				loadData('showSuggestions.php');
				break;
		
	
	}


}

function loadData(url)
{
document.getElementById('middle_left_top').style.opacity="0.8";
var loading=.7;	
var xmlHttp;
try
  {
  // Firefox, Opera 8.0+, Safari
  xmlHttp=new XMLHttpRequest();
  }
catch (e)
  {
  // Internet Explorer
  try
    {
    xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");
    }
  catch (e)
    {
    try
      {
      xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
      }
    catch (e)
      {
      alert("Your browser does not support AJAX!");
      return false;
      }
    }
  }
  xmlHttp.onreadystatechange=function()
    {
    	if(xmlHttp.readyState==4)
    	{
		document.getElementById('middle_left_top').innerHTML="<br/>"+xmlHttp.responseText;
		document.getElementById('middle_left_top').style.opacity=1;
		document.getElementById('middle_left_top').style.borderRight="1px solid #ccc";
		document.getElementById('middle_right').style.borderLeft="0px";
	}
	else{
	
		document.getElementById('middle_left_top').style.opacity=eval("'"+loading+"'");	
		loading-=.2;
	}
    }
  
 xmlHttp.open("GET",url,true);
 xmlHttp.send(null);
  }

function initializePage(){
	document.getElementById('intro_text').value=document.getElementById('middle_left_top').innerHTML;
	updateInfo(document.location.hash.split('#')[1],1);

 }
