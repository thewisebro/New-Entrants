<?php
session_start();
error_reporting(0);
// temporaraly commented for testing
include('connection.php');
if(!isset($_SESSION["username"]))
	header("Location: logout.php");



include('static.html');

//Collect Variables

$formInfo=array();


//In case new fields are added to this form, just need to specify here. If the field is mandatory add it to the array $mandatory
$formInfo["username"]=$_POST["username"];
$formInfo["company"]=$_POST["company"];
$formInfo["country"]=$_POST["country"];
$formInfo["city"]=$_POST["city"];
$formInfo["state"]=$_POST["state"];
$formInfo["current_desc"]=$_POST["desc"]; //Brief Summary Of Profile
$formInfo["industry"]=$_POST["industry"];
$formInfo["ind_spl"]=$_POST["ind_spl"]; //Industrial Specialization
$formInfo["other_ind"]=$_POST["other_ind"];
$formInfo["num_students"]=$_POST["num_students"];
$formInfo["mentor_area"]=$_POST["mentor_area"];
$formInfo["msg_consent"]=$_POST["msg_consent"];
$formInfo["aoi"]=$_POST["aoi"];


$mandatory=array("current_desc","industry","other_ind","num_students","mentor_area","msg_consent");



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
	upload2Db($dbcon,"mentor_data",$formInfo,"FullRegisterDone");
else

	{

		//Show the error message to the user
		show_message("'You have left some mandatory fields blank. Please click <a href=\'javascript:updateInfo(\"FullForm\")\'><b>here</b></a> to go back.'");
	

	}

/******************************************************************************************************************************/

include("disconnection.php");
?>
