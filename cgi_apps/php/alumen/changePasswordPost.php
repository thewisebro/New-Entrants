<?php
session_start();
error_reporting(0);
include('connection.php');
if(!isset($_SESSION["username"]))
	header("Location: logout.php");

if(isset($_SESSION["username"]))
	include('loggedin.html');
else	
	include('static.html');

//Collect Variables

$formInfo=array();


//In case new fields are added to this form, just need to specify here. If the field is mandatory add it to the array $mandatory
$formInfoTemp["old_password"]=$_POST["old_password"];
$formInfo["password"]=$_POST["new_password"];

$mandatory=array("password");



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

$formInfo["password"]=md5($formInfo["password"]);
$formInfoTemp["old_password"]=md5($formInfoTemp["old_password"]);

if(check_mandatory($formInfo,$mandatory)==1 && $username==$_SESSION["username"] && verifyOldPassword($dbcon,"basic_Data",$formInfoTemp["old_password"],$username))
	updateDb($dbcon,"basic_data",$formInfo,"password='".$formInfoTemp['old_password']."'","ChangePasswordDone");
else

	{

		//Show the error message to the user
		show_message("'Your password could not be changed. Carefully check the old password you entered. If the problem persists use \'Report a Bug\' to tell us about the problem.'");
	

	}

/******************************************************************************************************************************/

pg_close($dbcon);
?>
