<?php
include('../connection.php');

session_start();
if(!isset($_SESSION["student"]))
	header("Location: logout.php");



include('static.html');

//Collect Variables

$formInfo=array();


//In case new fields are added to this form, just need to specify here. If the field is mandatory add it to the array $mandatory
$formInfo["username"]=$_POST["username"];
$formInfo["current_desc"]=$_POST["desc"]; //Brief Summary Of Profile
$formInfo["mentor_area"]=$_POST["mentor_area"];
$formInfo["other_mentor_area"]=$_POST["other_mentor_area"];
$formInfo["msg_consent"]=$_POST["msg_consent"];
$formInfo["aoi"]=$_POST["aoi"];


$mandatory=array("current_desc","mentor_area","msg_consent");

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
if((check_mandatory($formInfo,$mandatory)==1) && ($_POST['username']==$_SESSION["student"]))
{

	if($photo)
	{
		if ($_FILES["Photo"]["error"] > 0)
	      	{
	        	echo "Error: " . $_FILES["Photo"]["error"] . "<br />";
	      	}
		else
		{
	     	  	$filename=$_FILES['Photo']['name'];
		  	$filelocation=$_FILES['Photo']['tmp_name'];
		  	$filesize_byte=$_FILES['Photo']['size'];
		  	$filesize=$filesize_byte/1024;
		  	$ext=pathinfo($_FILES['Photo']['name']);
		  	$fileext=$ext['extension'];
		  	//echo "<script language='javascript'>alert('File size is $filesize kb.')</script>";
		  	$filetype=$_FILES['Photo']['type'];
		  	//echo "<script language='javascript'>alert('File type is $filetype.')</script>";
		  	$uploaddir="uploads/".$username.".".$fileext;
		  	//echo "<script type=text/javascript>alert('$fileext')</script>";
		  	if($filesize>=25.00||($filetype!='image/jpeg' && $filetype!='image/gif' && $filetype!='image/png'))
		  	{
		  		echo "<script language='javascript'>alert('Can not submit. Either too big file or not a valid photo. File must be in jpeg, gif or png format less than 25 KB in size.')</script>";
		  	}
	    		else
	    		{
				if(move_uploaded_file($_FILES['photo']['tmp_name'],$uploaddir))
	    			{			
	        			$formInfo['photosrc']=$uploaddir;
            			}
            			else
	    			{
                			show_message("'Invalid Photo Upload. <a href=\'javascript:history.go(-1);\'>here</a> to go back.'");
                			exit();
            			}
            		}
		}
	}
}
else
{
		//Show the error message to the user
		show_message("'You have left some mandatory fields blank. Please click <a href=\'javascript:updateInfo(\"StudentBasicForm\")\'><b>here</b></a> to go back.'");
}

$fields = 'auth.username';
$student_id = $_POST['username'];
 $enroll = getStudentDetails($dbconchanneli, $fields, $student_id);
	$formInfo['enrollment_no']=$enroll[0][0];

	upload2Db($dbcon,"student_data",$formInfo,"StudentProfile");
/******************************************************************************************************************************/

include("../disconnection.php");
?>
