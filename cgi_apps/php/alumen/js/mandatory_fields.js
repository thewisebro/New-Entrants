//js for mandatory fields
function checkForm(formobj){

	// name of mandatory fields
	var fieldRequired = Array("name","email","username","password","repassword","day","month","year","passing_year","department","degree");
	// field description to appear in the dialog box
	var fieldDescription = Array("Name","Email","Username","Password","Confirm password","Day","Month","Year","PassingYear","Department","Degree");
	// dialog message
	var alertMsg = "Please complete the following fields:\n";
	//var alertMsg="";
	var l_Msg = alertMsg.length;
	if (formobj.password.value!=formobj.repassword.value)
	{
		alert("Passwords do not match !");
		return false;
	}
	
	
	var legalChars = /[a-z0-9_]/;
	  // allow only letters, numbers, and underscores
	       if (legalChars.test(formobj.username.value)!=true) {
	              alert( "The username contains illegal characters.");
			return false;

	       }
	if(formobj.username.value.length<6||formobj.username.value.length>10)
	{
		alert("Username is of wrong length.");
		return false;

	}

	re_passwd=/\W/;
	if(re_passwd.test(formobj.password.value)==true)
	{
		alert("Password contains invalid characters!");
		return false;

	}
	
	if(formobj.password.value.length<5||formobj.password.value.length>10)
	{
		alert("Password is of wrong length!");
		return false;
	}
	
	
	var re_email = /\b[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}\b/;
	// I also changed the validation to accept lowercase - this should be changed if undesired.
	if(re_email.test(formobj.email.value)!=true)
	{
		alert("Please enter a valid email address.");
		return false;

	}
	re_enroll=/\D/;
	if(re_enroll.test(formobj.enrollment_no.value)==true && formobj.enrollment_no.value.length>0)
	{
		alert("The enrollment number is invalid!");
		return false;
		
	}

	if (formobj.department.value=="AP" && !(formobj.degree.value=="B.Arch." || formobj.degree.value=="Other"))
	{

		alert("Incorrect information filled in Degree/Department");
		return false;
	}	

	//alertMsg+="Please complete the following fields:\n";
	for (var i = 0; i < fieldRequired.length; i++){
		var obj = formobj.elements[fieldRequired[i]];
		if (obj){
			switch(obj.type){
			case "select-one":
				if (obj.selectedIndex ==0 || obj.options[obj.selectedIndex].text == ""){
					alertMsg += " - " + fieldDescription[i] + "\n";
				}
				break;
			case "select-multiple":
				if (obj.selectedIndex == 0){
					alertMsg += " - " + fieldDescription[i] + "\n";
				}
				break;
			case "file":
			case "password":	
			case "text":
			case "textarea":
				if (validField(obj.value)==false ){
					alertMsg += " - " + fieldDescription[i] + "\n";
				}
				break;
			default:
			}
			if (obj.type == undefined){
				var blnchecked = false;
				for (var j = 0; j < obj.length; j++){
					if (obj[j].checked){
						blnchecked = true;
					}
				}
				if (!blnchecked){
					alertMsg += " - " + fieldDescription[i] + "\n";
				}
			}
		}
	}

	if (alertMsg.length == l_Msg){
		return true;
	}else{
		alert(alertMsg);
		return false;
	}
}
function stripBlanks(fld) {
var result = "";
var c = 0;
for (i=0; i<fld.length; i++) {
if (fld.charAt(i) != " " || c > 0) {
result += fld.charAt(i);
if (fld.charAt(i) != " ") c = result.length;
}
}
return result.substr(0,c);
}
function validField(fld) {
fld = stripBlanks(fld);
if (fld =="") return false;
return true;
}


//js for mandatory fields
function checkFullForm(formobj){

	// name of mandatory fields
	var fieldRequired = Array("desc","industry","num_students","msg_consent");
	// field description to appear in the dialog box
	var fieldDescription = Array("Profile Description","Industry","Number of students","Consent for messages");
	// dialog message
	var alertMsg = "Please complete the following fields:\n";
	//var alertMsg="";
	var l_Msg = alertMsg.length;

	if(formobj.mentor_area.value=="")
	{
		alertMsg+="-Choice of Mentor Area(s)\n";
	}

	//alertMsg+="Please complete the following fields:\n";
	for (var i = 0; i < fieldRequired.length; i++){
		var obj = formobj.elements[fieldRequired[i]];
		if (obj){
			switch(obj.type){
			case "select-one":
				if (obj.selectedIndex ==0 || obj.options[obj.selectedIndex].text == ""){
					alertMsg += " - " + fieldDescription[i] + "\n";
				}
				break;
			case "select-multiple":
				if (obj.selectedIndex == 0){
					alertMsg += " - " + fieldDescription[i] + "\n";
				}
				break;
			case "file":
			case "password":	
			case "text":
			case "textarea":
				if (validField(obj.value)==false ){
					alertMsg += " - " + fieldDescription[i] + "\n";
				}
				break;
			default:
			}
			if (obj.type == undefined){
				var blnchecked = false;
				for (var j = 0; j < obj.length; j++){
					if (obj[j].checked){
						blnchecked = true;
					}
				}
				if (!blnchecked){
					alertMsg += " - " + fieldDescription[i] + "\n";
				}
			}
		}
	}

	if (alertMsg.length == l_Msg){
		return true;
	}else{
		alert(alertMsg);
		return false;
	}
}
