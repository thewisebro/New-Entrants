function uploadPhoto(action)
{
	switch(action)
	{
		
		case "ChangePhoto";
				loadData('change_photo_form.php');
			break;
	
	}


}

function loadData(url)
{
document.getElementById('newPhoto').style.opacity="0.8";
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
		document.getElementById('newPhoto').innerHTML="<br/>"+xmlHttp.responseText;
		document.getElementById('newPhoto').style.opacity=1;
		document.getElementById('newPhoto').style.borderRight="1px solid #ccc";
		document.getElementById('newPhoto').style.borderLeft="0px";
	}
	else{
	
		document.getElementById('newPhoto').style.opacity=eval("'"+loading+"'");	
		loading-=.2;
	}
    }
  
 xmlHttp.open("GET",url,true);
 xmlHttp.send(null);
  }
