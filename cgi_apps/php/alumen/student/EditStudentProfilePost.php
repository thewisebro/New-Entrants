<?php
session_start();
//error_reporting(0);
include('../connection.php');

if(!isset($_SESSION['student']))
	header("Location: ../logout.php");	

$username=$_SESSION["student"];


include("../StudentLoggedIn.php");
//Collect Variables

$formInfo=array();


//In case new fields are added to this form, just need to specify here. If the field is mandatory add it to the array $mandatory

$formInfo["username"]=$_POST["username"];
$formInfo["current_desc"]=$_POST["desc"]; //Brief Summary Of Profile
$formInfo["mentor_area"]=$_POST["mentor_area"];
$formInfo["other_mentor_area"]=$_POST["other_mentor_area"];
$formInfo["aoi"]=$_POST["aoi"];
$formInfo["msg_consent"]=$_POST["msg_consent"];


/****************************************************************************/

$mandatory=array("current_desc","mentor_area");



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
if(check_mandatory($formInfo,$mandatory)==1 && $username==$_SESSION["student"]){
//	echo "<script language='javascript'>alert('herr')</script>";
	updateDb($dbcon,"student_data",$formInfo,"username='$username'","StudentProfile");
}else

	{

		//Show the error message to the user
		show_message("'You have left some mandatory fields blank. Please click <a href=\'javascript:updateInfo(\"EditStudentProfileForm\")\'><b>here</b></a> to go back.'");
	

	}

/******************************************************************************************************************************/

include("../disconnection.php");
?>
