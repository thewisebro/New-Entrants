<?php
session_start();
////////////////////////If approved sending a mail to the approved user///////////////////////////
//IITR SMTP : Important that asdmin's emails don't end up in spam
include("mail_iitr.php");

///////////////////////////////////////////////////////


if(!isset($_SESSION["admin_user"]))
	header("Location: adminLogout.php");

include('../connection.php');

$formInfo["status"]=$_GET["action"];
$formInfo["username"]=$_GET["user"];

$mandatory=array("status","username");

if (!get_magic_quotes_gpc()) 
{
	foreach($formInfo as $param => $info)
	{
		$formInfo[$param]=addslashes($info);

	}
}



/**************************functions**************************/
require('../common.php');
/***********************************************************/
if(check_mandatory($formInfo,$mandatory)==1) 
{
	switch($formInfo["status"])
	{

	case "approve":
			$formInfo["status"]="A";
			break;
	case "mark":
			$formInfo["status"]="M";
			break;
	case "reject":
			$formInfo["status"]="R";
			break;
	}

	//updateDb($dbcon,"basic_data",$formInfo,"username='".$formInfo["username"]."'","null");

	$query="Update basic_data set status = '".$formInfo['status']."' where username = '".$formInfo['username']."'";
	$execute=pg_query($dbcon,$query);

	$actionInfo=array();
	$actionInfo["action"]=$formInfo["username"]." changed to ".$formInfo["status"];
	$actionInfo["time"]=date("F j, Y, g:i a");

	upload2Db($dbcon,"admin_activity",$actionInfo,"null");
	
	if ($formInfo["status"]=="A")
	{
	$fields="email";
	$where_condition="username='".$formInfo["username"]."'";
	$emailArray=retrieveFromDb($dbcon,"basic_data",$fields,$where_condition);	
	$email=$emailArray[0];
	$message="Dear Alumnus,<br/>
	Congratulations on being a part of the Alumni Mentorship Programme of Indian Institute of Technology, Roorkee. We will be ready with the student profiles within one month.<br />
	We will send you updates regarding the programme on a regular basis. Your suggestions for making the programme a success are welcomed.<br /><br />
	Warm Regards,<br/>
	Information Management Group (IMG)<br/>
	IIT Roorkee.";



	email_to_user($email["email"],"img@iitr.ernet.in","IITR Alumni Mentorship Programme: Membership Approved","",$message);

	}

}	
else
{

		//Show the error message to the user
		show_message("'An invalid action was performed!'");
	

}





pg_close($dbcon);
?>
