<?php
session_start();
error_reporting(0);
include('connection.php');
include('mail.php');
if(isset($_SESSION["username"]))
	include('loggedin.html');
else
	include('static.html');

//Collect Variables

$formInfo=array();


//In case new fields are added to this form, just need to specify here. If the field is mandatory add it to the array $mandatory
$formInfo["contact"]=$_POST["contact"];
$formInfo["problem"]=$_POST["problem"];

$mandatory=array("contact","problem");



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
if(check_mandatory($formInfo,$mandatory)==1 && $username==$_SESSION["username"])
{	upload2Db($dbcon,"problem_data",$formInfo,"ProblemSubmittedForm");

	///////////////Remove this later/////////////////////////////////
	email_to_user("07ashis@gmail.com","img@iitr.ernet.in","AluMen:Problem Reported","",$formInfo["suggestion"]."--by".$formInfo['username']);	
	email_to_user("07ashis@gmail.com","img@iitr.ernet.in","AluMen:Problem Reported","",$formInfo["problem"]."--by".$formInfo['contact']);	


}
else

	{

		//Show the error message to the user
		show_message("'You did not fill either your contact information or the problem itself. Please click <a href=\'javascript:updateInfo(\"ProblemForm\",1)\'>here</a> to go back.'");
	

	}

/******************************************************************************************************************************/

pg_close($dbcon);
?>
