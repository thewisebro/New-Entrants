<?php
session_start();
error_reporting(-1);
include('connection.php');
include('static.html');
include('mail.php');
//Collect Variables

$formInfo=array();



//In case new fields are added to this form, just need to specify here. If the field is mandatory add it to the array $mandatory
$formInfo["username"]=$_POST["username"];
$formInfo["password"]=md5($_POST["password"]);
$formInfo["enrollment_no"]=$_POST["enrollment_no"];
$formInfo["fullname"]=$_POST["fullname"];
$formInfo["email"]=$_POST["email"];
$formInfo["department"]=$_POST["department"]; //Brief Summary Of Profile
$formInfo["degree"]=$_POST["degree"];
$formInfo["passing_year"]=$_POST["passing_year"];
$formInfo["status"]="W";
$mandatory=array("username","password","fullname","email","department","passing_year");



if (!get_magic_quotes_gpc()) 
{
	foreach($formInfo as $param => $info)
	{
		$formInfo[$param]=addslashes($info);

	}
}

/*****************************Functions***************************************************************************************/
require('common.php');
/**************************************************************************************************************************/

/********************************************Main Executable Part************************************************************************/
//First Check if all mandatory fields are filled(have some value). Javascript check is also performed. So this a double check.
if(user_already_exists($dbcon,$formInfo["username"],$formInfo["email"])==1)
{
	
	show_message("'The username or email address you chose already exists. <ul><li>Either login with the already registered username.</li><li>Or click <a href=\'javascript:history.go(-1);\'>here</a> to go back and choose another username.</li><li>If you have completed <b>Step 1</b> of registration you can proceed to <b>Step 2</b> by logging in.</ul>'");
	
}

else{
	if(check_mandatory($formInfo,$mandatory)==1){

		if($photo){
			$filesize=$_FILES['photo']['size'];
//			echo "<script language='javascript'>alert('$filesize')</script>";
			$filetype=$_FILES['photo']['type'];
//			echo "<script language='javascript'>alert('$filetype')</script>";

			$uploaddir="uploads/".$formInfo['username'].".jpeg";
			if(move_uploaded_file($_FILES['photo']['tmp_name'],$uploaddir)){
				$formInfo['photosrc']=$uploaddir;
			}
			else{
				show_message("'Invalid Photo Upload. <a href=\'javascript:history.go(-1);\'>here</a> to go back.'");
				exit();

			}

		}
		upload2Db($dbcon,"basic_data",$formInfo,"FullForm"); //Two Arguements: table name & information array
 	$fields="email";
        $where_condition="username='".$formInfo["username"]."'";
        $emailArray=retrieveFromDb($dbcon,"basic_data",$fields,$where_condition);
        $email=$emailArray[0];
        $message="Dear Alumnus,<br/>
        Thank you for registering for Alumni Mentorship Programme. Your request has been sent to the Dean of Alumni Affairs, Indian Institute of Technology Roorkee for approval. We will get back to you as soon as your details are verified.<br/><br/>
        Warm Regards,<br/>
        Information Management Group (IMG)<br/>
        IIT Roorkee.";


        email_to_user($email["email"],"img@iitr.ernet.in","IITR Alumni Mentorship Programme: Registration Complete","",$message);
}
	else

	{

		//Show the error message to the user
		show_message("'You have left some mandatory fields blank. Please click <a href=\'javascript:history.go(-1);\'>here</a> to go back.'");
	
	}
}

/******************************************************************************************************************************/

pg_close($dbcon);
?>
