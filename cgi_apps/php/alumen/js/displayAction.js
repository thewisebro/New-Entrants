function updateInfo(action,mode)
{
	switch(action)
	{
		case "Register":
				loadData('basicForm.php');
				break;
		case "Introduction":
				if(mode==0)
					document.getElementById('middle_left_top').innerHTML=document.getElementById('intro_text').value;
				else
					loadData('introduction.php');
				break;
		case "FullForm":
				loadData('fullForm.php');	
				break;
		case "FullRegisterDone":
				loadData('fullRegisterDone.php');
				break;
		case "SuggestionForm":
				loadData('suggestionForm.php');
				break;
		case "SuggestionSubmittedForm":
				loadData('suggestionSubmittedForm.php');
				break;
		case "ProblemForm":
				loadData('problemForm.php');
				break;
		case "ProblemSubmittedForm":
				loadData('problemSubmittedForm.php');
				break;
		case "ForgotpasswordForm":
				loadData('forgotPasswordForm.php');
				break;	
		case "EditProfileForm":
				loadData('editProfileForm.php');	
				break;
		case "EditProfileDoneForm":		
				loadData('editProfileDoneForm.php');
				break;
		case "ShowProfile":
				loadData('showProfile.php');
				break;
		case "ChangePasswordForm":
				loadData('changePasswordForm.php');
				break;
		case "ChangePasswordDone":
				loadData('changePasswordDone.php');
				break;		
		case "ForgotPasswordForm":
				loadData('forgotPasswordForm.php');
				break;
		case "ForgotPasswordDone":
				loadData('forgotPasswordDone.php');
				break;		
		case "Message":
				loadData('message.php');	
				break;
		case "Guidelines":
				loadData('guidelines.php');	
				break;
		case "ChangePhoto":
				loadData('showProfile_photo.php');
				break;
		case "StudentProfile":
				loadData('student/viewProfile.php');
				break;
		case "AlumniProfile":
				loadData('student/AlumniProfile.php');
				break;
		case "StudentBasicForm":
		        loadData('student/StudentBasicForm.php');
			    break;
		case "EditStudentProfileForm":
				loadData('student/EditStudentProfileForm.php');
				break;
		case "EditStudentProfileDone":
				loadData('EditStudentProfileDone.php');
				break;
		case "Mentorship":
				loadData('student/AlumniList.php');
				break;
		case "StudentList":
				loadData('student/StudentList.php');
				break;
		case "ViewStudentProfile":
				loadData('student/StudentProfile.php');
				break;
		case "Conversation":
				loadData('student/Conversation.php');
				break;
		case "Emails":
				loadData2('email-ids.php'+'?txtEmail='+document.getElementById("email").value);
				break;
		case "LeftEmails":
				loadData2('invitesLeft.php');
//		default:
//				loadData('');
//				break;
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
  
 xmlHttp.open("GET",url+"?origin=1",true);
 xmlHttp.send(null);
  }

function loadData2(url)
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
	
		document.getElementById('middle_left_top').style.opacity=1;
		document.getElementById('middle_left_top').style.borderRight="1px solid #ccc";
		document.getElementById('middle_right').style.borderLeft="0px";
		document.getElementById('previousEmails2').innerHTML=xmlHttp.responseText;
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
	runSlideShow();	

 }
function echeck(str) {

	var at="@";
		var dot=".";
		var lat=str.indexOf(at);
		var lstr=str.length;
		var ldot=str.indexOf(dot);
		if (str.indexOf(at)==-1){
			alert("Invalid E-mail ID");
				return false;
		}

	if (str.indexOf(at)==-1 || str.indexOf(at)==0 || str.indexOf(at)==lstr){
		alert("Invalid E-mail ID"); 
			return false;

	}

	if (str.indexOf(dot)==-1 || str.indexOf(dot)==0 || str.indexOf(dot)==lstr){
		alert("Invalid E-mail ID");
			return false;
	}

	if (str.indexOf(at,(lat+1))!=-1){
		alert("Invalid E-mail ID");
			return false;
	}

	if (str.substring(lat-1,lat)==dot || str.substring(lat+1,lat+2)==dot){
		alert("Invalid E-mail ID");
			return false;
	}

	if (str.indexOf(dot,(lat+2))==-1){
		alert("Invalid E-mail ID");
			return false;
	}

	if (str.indexOf(" ")!=-1){
		alert("Invalid E-mail ID");
			return false;
	}

	return true		;			
}

function ValidateForm(form){

	var emailID=document.getElementById("email");


		if ((emailID.value==null)||(emailID.value=="")){
			alert("Please Enter your Email ID");
				emailID.focus();
				return false;
		}
	if (echeck(emailID.value)==false){
		emailID.value="";
			emailID.focus();
			return false;
	}
	else
	{
	updateInfo("Emails",1);
	}

	return true;
}
