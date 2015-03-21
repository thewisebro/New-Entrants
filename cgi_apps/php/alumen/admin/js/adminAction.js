function adminAction(username,action)
{
	var url="http://people.iitr.ernet.in/AlumniMentorship/admin/adminAction.php";
	

	switch(action)
	{
		case "approve":
				url+="?action=approve&user="+username+"&codestring="+randomString();
				doAction(username,url,"Approved");
				break;
		case "part_invalid":
				url+="?action=mark&user="+username+"&codestring="+randomString();
				doAction(username,url,"Marked as 'Possibly Invalid'");
				break;
		case "invalid":
				url+="?action=reject&user="+username+"&codestring="+randomString();
				doAction(username,url,"Rejected");
				break;
	}
	var num=parseInt(document.getElementById("active_num").innerHTML);
	document.getElementById("active_num").innerHTML=num-1;


}


function doAction(username,url,action)
{
document.getElementById(username).style.opacity="0.8";
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
		document.getElementById(username).style.width="200px";
		document.getElementById(username).style.border="0px";
		document.getElementById(username).style.backgroundColor="#fff1a8";
		document.getElementById(username).innerHTML="<span id='notif'>"+action+"</span>";
		document.getElementById(username).style.opacity="1";
		disappear(username);
	}
	else{
	
		document.getElementById(username).style.opacity=eval("'"+loading+"'");	
		loading-=.2;
	}
    }
 xmlHttp.open("GET",url,true);
 xmlHttp.send(null);
  }
function randomString() {
	var chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";
	var string_length = 8;
	var randomstring = '';
	for (var i=0; i<string_length; i++) {
		var rnum = Math.floor(Math.random() * chars.length);
		randomstring += chars.substring(rnum,rnum+1);
	}
	return randomstring;
}

function disappear(id)
{
	setTimeout('document.getElementById(\''+id+'\').style.display=\'none\'',3000);

}
