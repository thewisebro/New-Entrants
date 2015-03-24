<?php
session_start();
if(!isset($_SESSION["student"]))
{
    header("location: logout.php");
}

include("../connection.php");
include("common.php");
include("mail_iitr.php");

$alumni=$_GET['alumni'];
$student=$_SESSION['student'];
$student_status=getStudentStatus($_SESSION['student'],$dbcon);

if($student_status<3)
{
	$status_al = getStudentStatus_Al($alumni,$student,$dbcon);
	if($status_al=="Not Defined")
	{
		$student_wl = retrieveFromDb($dbcon,"student_data","wl","username=$student");
		$wl=$student_wl[0][0];
		$al_sts = getAlumniStatus($alumni,$dbcon);
		
		if($al_sts=='WL')
		{
			if($wl==1)
			{
				$_SESSION['message']="You cannot apply to waiting list of more than one alumni";
			}
			else
			{
				$query="Update student_data set wl=1 where username=$student";
				$execute=pg_query($dbcon,$query);
			}
		}
		if($wl==0)
		{
			$formInfo['alumni']=$alumni;
			$formInfo['student']=$student;
			$formInfo['timst']=time();
			$formInfo['al_sts']=$al_sts;
			$formInfo['status']='A';
	
			$alumni_fullname=retrieveFromDb($dbcon,"basic_data","fullname","username='$alumni'");
			$alumni_name=$alumni_fullname[0][0];
			$_SESSION['message']="You have succesfully applied to $alumni_name for mentorship.";
			upload_application($dbcon,"mentorship",$formInfo);
			
      $fields = "nperson.name as name, nbranch.name as discipline_full";
      $student_id = $student ;
      $student_details = getStudentDetails($dbconchanneli, $fields, $student_id);
      $value =  $student_details[0]['discipline_full'];

			$fields="email";
			$where_condition="username='$alumni'";
			$emailArray=retrieveFromDb($dbcon,"basic_data",$fields,$where_condition);
			$email=$emailArray[0];
			$message="Dear Alumnus,<br/>
			The following student has applied to you for mentorship : <br/>
			<table border ='1' style ='empty-cells:show; text-align:left; margin-top:10px' cellspacing='0' cellpadding='5'>
			<tr>
			 <td> Name : </td>
			 <td>".$student_details[0][0]."</td>
			</tr>
			<tr>
			 <td> Discipline : </td>
			 <td>$value</td>
			</tr>
			</table><br />
			Please visit <a href='http://people.iitr.ernet.in/' target ='_blank'>Alumni Mentorship</a> portal to consider his application.<br/><br/>
			Warm Regards,<br/>
			Information Management Group (IMG)<br/>
			IIT Roorkee.";
		        email_to_user($email["email"],"img@iitr.ernet.in","IITR Alumni Mentorship Programme: Mentorship Application","",$message);
		}
	}
	else
	{
		switch($status_al)
		{
		  case 'Not Approved':
		  			$_SESSION['message']="You cannot apply to this alumi as he has already refused your request for mentorship.";
						break;
		  case 'Waiting Approval':
		  			$_SESSION['message']="You have already applied to this alumni";	
						break;
		  case 'Finalized':
		  			$_SESSION['message']="The alumni has already accepted your request for mentorship.";
						break;
		}
	}
}
else
{
	echo "You cannot apply to this alumni as you have already applied to three alumni.";
}

include("../disconnection.php");

echo "<script language='javascript'>";
echo "document.location='http://people.iitr.ernet.in/AlumniMentorship/student.php#Mentorship';";
echo "updateInfo('Mentorship')";
echo "</script>";

?>

