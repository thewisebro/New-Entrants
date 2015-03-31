<?php
session_start();
if(!isset($_SESSION["username"])) 
{
	header("Location: logout.php");
	die();
}

include("../connection.php");
include_once("common.php");

$alumni=$_GET['alumni'];
$student=$_GET['student'];
$status=$_GET['status'];


if($_SESSION['username']==$alumni)
{
	switch($status)
	{
		case 'app':
				$sts='A+';
				updateStudentStatus($student,$alumni,$sts,$dbcon);
				break;
		case 'rej':
				$sts='A-';
				updateStudentStatus($student,$alumni,$sts,$dbcon);
				updateAl_sts($alumni,$dbcon);	
				break;
		case 'fin':
				$sts='F';
				updateStudentStatus($student,$alumni,$sts,$dbcon);
				deleteOtherAppsOfStudent($student,$dbcon);
				break;
		default:
				$sts ='A';
	}

	$mentorship = getMentorshipStatus($alumni,$dbcon);
	echo $mentorship;
	if($mentorship)
	{
		notifyOtherStudentApplicants($alumni,$dbcon);
	}
}	
include('../disconnection.php');

echo "<script language='javascript'>";
echo "document.location='http://people.iitr.ernet.in/AlumniMentorship/loginSuccess.php#StudentList';";
echo "updateInfo('StudentList',1)";
echo "</script>";

?>
