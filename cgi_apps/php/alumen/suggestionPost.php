<?php
session_start();
error_reporting(0);
include('connection.php');

////////////////
include('mail.php');

///////////////////


if(isset($_SESSION["username"]))
	include('loggedin.html');
else	
	include('static.html');

//Collect Variables

$formInfo=array();


//In case new fields are added to this form, just need to specify here. If the field is mandatory add it to the array $mandatory
$formInfo["username"]=$_POST["username"];
$formInfo["suggestion"]=$_POST["suggestion"];

$mandatory=array("suggestion");



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
//First Check if all mandatory fields are filled(have some value). Javascript check is also performed(not implemented for all forms though!). So this a double check.
if(check_mandatory($formInfo,$mandatory)==1 && $username==$_SESSION["username"])
{	
	upload2Db($dbcon,"suggestion_data",$formInfo,"SuggestionSubmittedForm");
	
	///////////////Remove this later/////////////////////////////////
	email_to_user("07ashis@gmail.com","img@iitr.ernet.in","AluMen:Suggestion","",$formInfo["suggestion"]."--by".$formInfo['username']);	
	email_to_user("07ashis@gmail.com","img@iitr.ernet.in","AluMen:Suggestion","",$formInfo["suggestion"]."--by".$formInfo['username']);	


	/////////////////////////////////////////////////////////////////
}

else

	{

		//Show the error message to the user
		show_message("'You did not submit any suggestion. Please click <a href=\'javascript:updateInfo(\"SuggestionForm\")\'>here</a> to go back.'");
	

	}

/******************************************************************************************************************************/

pg_close($dbcon);
?>
