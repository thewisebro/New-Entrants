<?php
session_start();
//error_reporting(0);
include('connection.php');

if(!isset($_SESSION["username"]))
	header("Location: logout.php");	

$username=$_SESSION["username"];


include('loggedin.html');

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
$formInfo["other_mentor_area"]=$_POST["other_mentor_area"];
$formInfo["aoi"]=$_POST["aoi"];
$formInfo["msg_consent"]=$_POST["msg_consent"];


/**************special temporary variables:not present in db****************/
$formInfoTemp=array();
$formInfoTemp["updated_country"]=$_POST["updated_country"];
$formInfoTemp["updated_industry"]=$_POST["updated_industry"];
$formInfoTemp["updated_ind_spl"]=$_POST["updated_ind_spl"]; //Industrial Specialization
$formInfoTemp["updated_other_ind"]=$_POST["updated_other_ind"];
$formInfoTemp["updated_num_students"]=$_POST["updated_num_students"];



/****************************************************************************/

$mandatory=array("current_desc","industry","num_students","mentor_area");



if (!get_magic_quotes_gpc()) 
{
	foreach($formInfo as $param => $info)
	{
		$formInfo[$param]=addslashes($info);

	}
}
if (!get_magic_quotes_gpc()) 
{
	foreach($formInfoTemp as $param => $info)
	{
		$formInfoTemp[$param]=addslashes($info);

	}
}
/**********************check if special fields(mentioned above) were really updated or not & then remove them**********/

if($formInfoTemp['updated_country']!='None')
{
	$formInfo['country']=$formInfoTemp['updated_country'];

}
if($formInfoTemp['updated_industry']!='None')
{
	$formInfo['industry']=$formInfoTemp['updated_industry'];

}
if($formInfoTemp['updated_ind_spl']!='None')
{
	$formInfo['ind_spl']=$formInfoTemp['updated_ind_spl'];

}
if($formInfoTemp['updated_num_students']!='None')
{
	$formInfo['num_students']=$formInfoTemp['updated_num_students'];

}

/*****************************Functions***************************************************************************************/

require('common.php');

/**************************************************************************************************************************/

/********************************************Main Executable Part************************************************************************/
//First Check if all mandatory fields are filled(have some value). Javascript check is also performed. So this a double check.
if(check_mandatory($formInfo,$mandatory)==1 && $username==$_SESSION["username"]){
	//echo "<script language='javascript'>alert('herr')</script>";
	updateDb($dbcon,"mentor_data",$formInfo,"username='$username'","EditProfileDoneForm");
}else

	{

		//Show the error message to the user
		show_message("'You have left some mandatory fields blank. Please click <a href=\'javascript:updateInfo(\"EditProfileForm\")\'><b>here</b></a> to go back.'");
	

	}

/******************************************************************************************************************************/

pg_close($dbcon);
?>
