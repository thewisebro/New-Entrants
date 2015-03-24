<?php

session_start();
if(!isset($_SESSION["student"]))
{
    header("location: logout.php");
}

include_once('../connection.php');
require('common.php');

$student =$_SESSION['student'];

if(MentorshipAscess($student,$dbconchanneli)|| $student='shaziume')
{

if(isset($_SESSION['message']))
{
	echo $_SESSION['message']."<br/><br />";
	unset($_SESSION['message']);
}

echo "<b>Note: You can apply to only three Alumni for mentorship.</b><br />";

$chk_finalized = retrieveFromDb($dbcon,"mentorship","alumni","student='$student' and status='F'");
$chk_approved = retrieveFromDb($dbcon,"mentorship","alumni","student='$student' and status='A+'");
$chk_applied = retrieveFromDb($dbcon,"mentorship","alumni","student='$student' and status='A'"); 
$chk_rejected = retrieveFromDb($dbcon,"mentorship","alumni","student='$student' and status='A-'");

if(count($chk_finalized)!=0)
{
	
	$alumni=$chk_finalized[0][0];
	$fields="enrollment_no,fullname,email,department,degree,passing_year,photosrc";
	$where_condition="username='$alumni'";
	$basicInfoArray=retrieveFromDb($dbcon,"basic_data",$fields,$where_condition);
	$basicInfo=$basicInfoArray[0];
	
	echo"<fieldset>";
	echo"	<legend>Your Mentor</legend>
			<table border='0'>
			<tr>
			<td><img height='150px' width='150px' src='";
	if($basicInfo['photosrc']==NULL)
		echo "images/default.JPG";
	else 
		echo "uploads/".$basicInfo['photosrc'];
		
	echo"' alt='photo' /></td>";
	
	echo"
			<td>&nbsp;</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
			<td>
				<table border='0'>
				<tr>
				<td><b>Name</b></td>
				<td>".$basicInfo['fullname']."</td>
				</tr>
			
				<tr>
				<td><b>Degree</b></td>
				<td>".$basicInfo['degree']."</td>
				</tr>
	
				<tr>
				<td><b>Department</b></td>
				<td>".$basicInfo['department']."</td>
				</tr>
	
			
				<tr>
				<td><b>Profile</b></td>
				<td><a href='student/connector.php?alumni=".$alumni."' target='_blank'>Full Profile</a></td>
				</tr>
				
				</table>
			</td>
			</tr>
			</table>
		</fieldset>";
}

else 
{
	if(count($chk_approved)!=0)
	{
		echo "<fieldset><legend>Approved Applications</legend>";
		echo "The following alumni have approved your application for consideration:- <br />";
	
		$limit = count($chk_approved);
		
		echo "<br /><table border ='1' style ='empty-cells:show; text-align:left' cellspacing='0' cellpadding='5'>";
		echo "<th>S. No.</th><th>Name</th><th>Degree</th><th>Department</th><th>E-mail</th>";
		
		for($i=0;$i<$limit;$i++)
		{
			echo "<tr><td>".($i+1)."</td>";
			$fields="fullname,email,department,degree";
			$where_condition="username='".$chk_approved[$i][0]."'";
			$basicInfoArray=retrieveFromDb($dbcon,"basic_data",$fields,$where_condition);
			$basicInfo=$basicInfoArray[0];
			echo "<td><a href='student/connector.php?alumni=".$chk_approved[$i][0]."' target ='_blank'>".$basicInfo['fullname']."</td>";
			echo "<td>".$basicInfo['degree']."</td>";
			echo "<td>".$basicInfo['department']."</td>";
		
			echo "</tr>";
		}
			
		echo "</table></fieldset>";
	}

	if(count($chk_applied)!=0)
	{
	        echo "<fieldset><legend>Your Applications</legend>";
	        echo "You have applied to the following alumni for mentorship:- <br />";

		$limit = count($chk_applied);
                echo "<br /><table border ='1' style ='empty-cells:show; text-align:left' cellspacing='0' cellpadding='5'>";
                echo "<th>S. No.</th><th>Name</th><th>Degree</th><th>Passing Year</th>";
                for($i=0;$i<$limit;$i++)
                {
                       echo "<tr><td>".($i+1)."</td>";
                       $fields="fullname,email,passing_year,degree";
                       $where_condition="username='".$chk_applied[$i][0]."'";
                       $basicInfoArray=retrieveFromDb($dbcon,"basic_data",$fields,$where_condition);
                       $basicInfo=$basicInfoArray[0];
                       echo "<td><a href='student/connector.php?alumni=".$chk_applied[$i][0]."' target ='_blank'>".$basicInfo['fullname']."</td>";
                       echo "<td>".$basicInfo['degree']."</td>";
                       echo "<td>".$basicInfo['passing_year']."</td>";
                       echo "</tr>";
                 }
 
 		echo "</table></fieldset>";
	}

	if(count($chk_rejected)!=0)
	{
		echo "<fieldset><legend>Rejected Applications</legend>";
		echo "The following alumni have rejected your application for mentorship:- <br />";
	
		$limit = count($chk_rejected);
		
		echo "<br /><table border ='1' style ='empty-cells:show; text-align:left' cellspacing='0' cellpadding='5'>";
		echo "<th>S. No.</th><th>Name</th><th>Degree</th>";
		
		for($i=0;$i<$limit;$i++)
		{
			echo "<tr><td>".($i+1)."</td>";
			$fields="fullname,email,department,degree";
			$where_condition="username='".$chk_rejected[$i][0]."'";
			$basicInfoArray=retrieveFromDb($dbcon,"basic_data",$fields,$where_condition);
			$basicInfo=$basicInfoArray[0];
			echo "<td><a href='student/connector.php?alumni=".$chk_rejected[$i][0]."' target ='_blank'>".$basicInfo['fullname']."</td>";
			echo "<td>".$basicInfo['degree']."</td>";
			echo "</tr>";
		}
			
		echo "</table></fieldset>";
	}

	if(getStudentStatus($student,$dbcon)<3)
	{
		main_list($dbcon,$student);
	}
}
}

else
{
	echo "Only B.Tech/IDD students of 3, 4, 5 years are intended to participate in this programme.";
}

function main_list($dbcon,$student)
{
	if(isset($_SESSION['al_page']))
	{
		$page=$_SESSION['al_page'];
	}
	else
	{	
		$page=1;
	}
	
	$table="basic_data";
	$limit =10;
	$start = $limit*($page-1)+1;
	$end = $start + $limit - 1;
	
//	$query_display = "Select a.username,a.fullname,a.passing_year from basic_data a, mentor_data b where a.username=b.username and a.status='A' order by fullname offset ($start-1) limit $limit";

	$query_display="Select a.username,a.fullname,a.passing_year from basic_data a, mentor_data b where a.username=b.username order by fullname offset ($start-1) limit $limit";
	$display_result = pg_query($dbcon,$query_display);
	
	//echo "<div align ='center'>";
	echo "<fieldset><legend>Mentors</legend> <br />";
	echo "<table border ='1' style ='empty-cells:show; text-align:left' cellspacing='0' cellpadding='5'>";
	echo "<th>S. No.</th><th>Name</th><th>Passing Year</th><th style ='text-align:center'>Industry</th><th>MNS</th><th>Status</th><th>Mentorship</th>";

	$dis_res=pg_query($dbcon,"Select a.username,a.fullname,a.passing_year from basic_data a, mentor_data b where a.username=b.username"); //and a.status='A'"); 
	$count = pg_num_rows($dis_res);

	$stdno = getStudentStatus($student,$dbcon);

	for($i=$start;$row = pg_fetch_array($display_result);$i++)
	{
		$alumni = $row['username'];

		echo "<tr>";
		echo "<td> $i </td>";
		echo "<td><a href='student/connector.php?alumni=$alumni' target='_blank'>". $row['fullname']."</a></td>";
		echo "<td>". $row['passing_year']." </td>";
		
		$info= retrieveFromDB($dbcon,"mentor_data","industry,num_students","username='$alumni'");
		$status_1 = getAlumniStatus($alumni,$dbcon);
		$status = getCodeValue($status_1,$dbcon);
		
		echo "<td>".getCodeValue($info[0][0],$dbcon)."</td>";
		echo "<td>".$info[0][1]."</td>";
			
		echo "<td>$status</td>";
	
		$std = getStudentStatus_Al($alumni,$student,$dbcon);
		
		if(($stdno<4)&&($std=="Not Defined")&&($status!='Closed'))
		{
			echo "<td><a href='student/Mentorship.php?alumni=$alumni'>Apply</a></td>";
		}
		else 
			echo "<td>$std</td>";

		echo "</tr>";
		
	}
	
	echo "</table>";
	echo "<br />";
	echo "<div align ='center' style ='width =100%'>";

	if($count<=$limit);
	else if(($end<$count)&&($start>$limit))
	{
		$ppage=$page-1;
		$page++;
		echo "<a href = student/AlumniListSetPage.php?page=$ppage> PREVIOUS </a>...";
		echo "<a href = student/AlumniListSetPage.php?page=$page> NEXT </a>";
	}
	else if($start>=($count-$limit))
	{
		 $ppage=$page-1;
		 echo "<a href = student/AlumniListSetPage.php?page=$ppage> PREVIOUS </a>";
	}
	else if($end<=$limit)
	{
		 $page++;
		 echo "<a href = student/AlumniListSetPage.php?page=$page> NEXT </a>";
	}
	echo "</div></fieldset>";
}

include("../disconnection.php");
?>
