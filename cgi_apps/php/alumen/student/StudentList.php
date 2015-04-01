<?php
session_start();
if(!isset($_SESSION["username"])) 
{
	header("Location: logout.php");
	die();
}

include("../connection.php");
include_once("common.php");

$alumni = $_SESSION["username"];

if(MentorshipAscessOfAlumni($alumni,$dbcon))
{
$students_applied = retrieveFromDb($dbcon,"mentorship","student","alumni='$alumni' and status='A' and al_sts='O' order by timst ");
$students_approved = retrieveFromDb($dbcon,"mentorship","student","alumni='$alumni' and status='A+' order by timst ");
$students_rejected = retrieveFromDb($dbcon,"mentorship","student","alumni='$alumni' and status='A-' order by timst ");
$students_finalized = retrieveFromDb($dbcon,"mentorship","student","alumni='$alumni' and status='F' order by timst ");
$students_cancelled = retrieveFromDb($dbcon,"mentorship","student","alumni='$alumni' and status='X' order by timst ");

if($students_finalized)
{
	echo "<fieldset><legend>Finalized Students</legend>";
	echo "The following students have been finalized by you for mentorship:- <br />";

	$limit = count($students_finalized);
	
	echo "<br /><table border ='1' style ='empty-cells:show; text-align:left' cellspacing='0' cellpadding='5'>";
	echo "<th>S. No.</th><th>Name</th><th>Discipline</th><th>Contact</th>";
	
	for($i=0;$i<$limit;$i++)
	{
		echo "<tr><td>".($i+1)."</td>";
    $fields = 'nperson.name as name, nbranch as discipline_full, nperson.email_id as alternate_email, nperson.personal_contact_no as contact_phone_no';
    $student_id = $students_finalized[$i][0];
    $student_details = getStudentDetails($dbconchanneli, $fields, $student_id);
		echo "<td><a href='student/st_connector.php?student=".$students_finalized[$i][0]."' target ='_blank'>".$student_details[0][0]."</td>";
    $value = $student_details[0]['discipline_full'];
		echo "<td>$value</td>";
//		echo "<td>".$student_details[0][2]."</td>";
		echo "<td>".$student_details[0][3]."</td>";
		echo "</tr>";
	}
		
	echo "</table></fieldset><br />";
}

if(getMentorshipStatus($alumni,$dbcon)==0)
{
	if($students_cancelled)
	{
		echo "<fieldset><legend>Cancelled Applications</legend>";
		echo "The applications of the following students have been cancelled because they have been selected by another alumni for mentorship:- <br />";
	
		$limit = count($students_cancelled);
	
		echo "<br /><table border ='1' style ='empty-cells:show; text-align:left' cellspacing='0' cellpadding='5'>";
		echo "<th>S. No.</th><th>Name</th><th>Discipline</th>";
	
		for($i=0;$i<$limit;$i++)
		{
			 echo "<tr><td>".($i+1)."</td>";
	   $fields = 'nperson.name as name, nbranch as discipline_full, nperson.email_id as alternate_email, nperson.personal_contact_no as contact_phone_no';
    $student_id = $students_cancelled[$i][0];
    $student_details = getStudentDetails($dbconchanneli, $fields, $student_id);
    $value = $student_details[0]['discipline_full'];
			 echo "<td><a href='student/st_connector.php?student=".$students_cancelled[$i][0]."' target ='_blank'>".$student_details[0][0]."</td>";
			 echo "<td>$value</td>";
			 echo "</tr>";
		}
																									
		echo "</table></fieldset><br />";
	}
	
	if($students_approved)
	{
		echo "<fieldset><legend>Approved Students</legend>";
		echo "The following students have been approved by you for consideration:- <br />";
	
		$limit = count($students_approved);
	
		echo "<br /><table border ='1' style ='empty-cells:show; text-align:left' cellspacing='0' cellpadding='5'>";
		echo "<th>S. No.</th><th>Name</th><th>Discipline</th><th>E-mail</th><th>Contact</th><th>Finalize</th><th>Reject</th>";
	
		for($i=0;$i<$limit;$i++)
		{
			 echo "<tr><td>".($i+1)."</td>";
		$fields = 'nperson.name as name, nbranch as discipline_full, nperson.email_id as alternate_email, nperson.personal_contact_no as contact_phone_no';
    $student_id = $students_approved[$i][0];
    $student_details = getStudentDetails($dbconchanneli, $fields, $student_id);
    $value = $student_details[0]['discipline_full'];
			 echo "<td><a href='student/st_connector.php?student=".$students_approved[$i][0]."' target ='_blank'>".$student_details[0][0]."</td>";
			 echo "<td>$value</td>";
			 echo "<td>".$student_details[0][2]."</td>";
			 echo "<td>".$student_details[0][3]."</td>";
			 echo "<td><a href='student/MentorshipProcess.php?alumni=$alumni&student=".$students_approved[$i][0]."&status=fin'>Finalize</td>";
			 echo "<td><a href='student/MentorshipProcess.php?alumni=$alumni&student=".$students_approved[$i][0]."&status=rej'>Reject</td>";
			 echo "</tr>";
		}
																									
		echo "</table></fieldset><br />";
	}
	
	echo "<fieldset><legend>Mentorship Applications</legend>";
	echo "The following students have applied to you for mentorship:- <br />";
	
	if($students_applied)
	{
		$limit = count($students_applied);
	
			echo "<br /><table border ='1' style ='empty-cells:show; text-align:left' cellspacing='0' cellpadding='5'>";
			echo "<th>S. No.</th><th>Name</th><th>Discipline</th><th>Approve</th><th>Reject</th>";
	
		for($i=0;$i<$limit;$i++)
		{
			 echo "<tr><td>".($i+1)."</td>";
	   $fields = 'nperson.name as name, nbranch as discipline_full, nperson.email_id as alternate_email, nperson.personal_contact_no as contact_phone_no';
    $student_id = $students_applied[$i][0];
    $student_details = getStudentDetails($dbconchanneli, $fields, $student_id);
    $value = $student_details[0]['discipline_full'];
			 echo "<td><a href='student/st_connector.php?student=".$students_applied[$i][0]."' target ='_blank'>".$student_details[0][0]."</td>";
			 echo "<td>$value</td>";
			 echo "<td><a href='student/MentorshipProcess.php?alumni=$alumni&student=".$students_applied[$i][0]."&status=app'>Approve</td>";
			 echo "<td><a href='student/MentorshipProcess.php?alumni=$alumni&student=".$students_applied[$i][0]."&status=rej'>Reject</td>";
			 echo "</tr>";
		}
		echo "</table>";
	
	}
	else
	{
		echo "<br />There aren't any applications for your consideration at the moment. Please check back later for new applications.<br />";
	}
	echo "</fieldset><br />";
	
	if($students_rejected)
	{
		echo "<fieldset><legend>Rejected Applications</legend>";
		echo "The mentorship application of following students have been rejected by you:- <br />";
	
		$limit = count($students_rejected);
	
		echo "<br /><table border ='1' style ='empty-cells:show; text-align:left' cellspacing='0' cellpadding='5'>";
		echo "<th>S. No.</th><th>Name</th><th>Discipline</th><th>Approve</th><th>Reject</th>";
	
		for($i=0;$i<$limit;$i++)
		{
			 echo "<tr><td>".($i+1)."</td>";
	   $fields = 'nperson.name as name, nbranch as discipline_full, nperson.email_id as alternate_email, nperson.personal_contact_no as contact_phone_no';
    $student_id = $students_rejected[$i][0];
    $student_details = getStudentDetails($dbconchanneli, $fields, $student_id);
    $value = $student_details[0]['discipline_full'];
			 echo "<td><a href='student/st_connector.php?student=".$students_rejected[$i][0]."' target ='_blank'>".$student_details[0][0]."</td>";
			 echo "<td>$value</td>";
			 echo "<td><a href='student/MentorshipProcess.php?alumni=$alumni&student=".$students_rejected[$i][0]."&status=app'>Approve</td>";
			 echo "</tr>";		    
		}     
		
		echo "</table></fieldset><br />";
	}
}
}
else
{
	echo "Please wait for your status as an alumni of IIT Roorkee to be verified before mentorship process can begin.";
}
include("../disconnection.php");
?>
