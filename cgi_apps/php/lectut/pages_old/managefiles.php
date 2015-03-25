<?php

//session_start();
include_once("../common/functions.php");
include("../../session/django_session.php");
$session = new Session();
$loggedIn=false;

//if(isLogin($_SESSION['username'],$_SESSION['sessionid']))
//{
if($session->isloggedin()){
  if($_SESSION['group']=='s')	
		$studId=$_SESSION['lectut_userid'];
	if($_SESSION['group']==0)
		$facId=$_SESSION['lectut_userid'];
	$loggedIn=true;
}
else
{
	$loggedIn=false;
}

if($loggedIn && $_SESSION['group']=='s')
{
	header("Location: student.php");
}
$facUsername=$_SESSION['lectut_username'];

?>


<html>
<head>
<title>Lectures and Tutorials</title>

<link rel=stylesheet href="../styles_old/lectntut.css" type="text/css">
	<script src="../common/jscriptfunc.js"></script>

</head>

<body>


<div id="container">

	<div id="top_links">

<?php
if($loggedIn && $_SESSION['group']==0)
{
		disp_fac_design_choice($loggedIn,$facId);
}
?>
		<div class="curve_edge_lt">&nbsp;</div>
		<div class="link"><a href="/" target="_blank">Channel I</a></div>
		<div class="curve_edge_rt"><a href="mailto:img@iitr.ernet.in" target="_blank"></a></div>
		<div class="curve_edge_lt">&nbsp;</div>
		<div class="link"><a href="mailto:img@iitr.ernet.in" target="_blank">Complaints/Suggestions</a></div>
		<div class="curve_edge_rt"><a href="mailto:img@iitr.ernet.in" target="_blank"></a></div>
		<div class="curve_edge_lt"></div>
		<div class="link"><a href="logout.php">Logout</a></div>
		<div class="curve_edge_rt"></div>
	</div>
	<!---Top Links div end here-->

	
	<div id="header_links">
		<div id="header">&nbsp;</div>
		<div id="links_right">
			<div class="links"><a href="faculty.php">Upload lectures and tutorials</a></div>
		<div class="links"><a href="managefiles.php">Manage files</a></div>
		<div class="links"><a href="dept_list.php">View &nbsp;&nbsp; lectures and Tutorials</a></div>
	</div>
</div>
	<!--Header ends here-->
	
	<div id="middle_block">
			<? 
$temp2=$_GET['temp2'];
if(isset($temp2))
{
	$logfile=fopen("../lectut_profs_logs.txt",'a');
	$logstring="";

	$d=$_GET['d'];
	$nd=$_GET['nd'];
	$ne=$_GET['ne'];
	if($d>0)
		echo "$d files deleted.<br>";
	if($nd>0)
		echo "$nd files not deleted. Please try again later.<br>";
	if($ne>0)
		echo "$ne files donot exist.<br>";

	$logstring=date("D F d Y",time())." ".$facUsername." $d files deleted. $nd files not deleted. Please try again later. $ne files donot exist.\n"; 	
	fwrite($logfile,$logstring);
	fclose($logfile);
}


?>

		<table id="file_list">
		<form name="delete" action="delete.php" method="post" onsubmit="return validate_form();">

		<?
database::connectToDatabase();

$return_l=database::executeQuery(database::getDistinctId(COURSE_ID,LEC_TABLE,"WHERE ".FACULTY_ID."='$facUsername'"));
$return_t=database::executeQuery(database::getDistinctId(COURSE_ID,TUT_TABLE,"WHERE ".FACULTY_ID."='$facUsername'"));
$return_e=database::executeQuery(database::getDistinctId(COURSE_ID,EXAM_TABLE,"WHERE ".FACULTY_ID."='$facUsername'"));
$return_s=database::executeQuery(database::getDistinctId(COURSE_ID,SOLN_TABLE,"WHERE ".FACULTY_ID."='$facUsername'"));

if(isset($studId))
{
	$reg_courses=database::executeQuery(database::studQuery($studId));
}

$l=1;
$t=1;
$e=1;
$s=1;

	// Lectures List start.
while($row=mysql_fetch_array($return_l))
{
	$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
	$row1=mysql_fetch_row($result1);
	if($row1[0]==null)
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=mysql_fetch_row($result1);			
	}
?>
		<tr class="heading">
			<td class="sub_code"><?echo $row[0] //Subject Code?></td>
			<td class="type"><!--Type--></td>
			<td class="delete"><!--Delete files--></td>
		</tr>
<?php
		$return_lec=database::getLecObject("COURSE_ID",$row[0],null);
	$i=0;
	
	foreach($return_lec as $result)
	{
		if(($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses)) && $result->getFacultyId()==$facUsername)
		{
			$i++;


?>
				<tr class="list">
				<td><a href="<? echo LECDIR; ?>/<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>">
<?echo $result->getTopic(); ?></a></td>
<td>Lectures</td>
<td><input type="checkbox" name="lec[]" class="chk" id="lec_<?php echo $l++; ?>" value="<? echo $result->getId(); ?>/<? echo $result->getFile(); ?>"></td>
				</tr>			
	
<?php
		}
	}
	if($i==0)
	{
		echo "No lectures.";
	}

}
	// Lectures end.

	// Tutorials List start.
while($row=mysql_fetch_array($return_t))
{
	$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
	$row1=mysql_fetch_row($result1);
	if($row1[0]==null)
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=mysql_fetch_row($result1);			
	}
?>
		<tr class="heading">
			<td class="sub_code"><?echo $row[0] //Subject Code?></td>
			<td class="type"><!--Type--></td>
			<td class="delete"><!--Delete files--></td>
		</tr>
<?php
		$return_tut=database::getTutObject("COURSE_ID",$row[0],null);
	$i=0;
	
	foreach($return_tut as $result)
	{
		if(($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses)) && $result->getFacultyId()==$facUsername)
		{
			$i++;


?>
				<tr class="list">
				<td><a href="<? echo TUTDIR; ?>/<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>">
<?echo $result->getTopic(); ?></a></td>
<td>Tutorials</td>
<td><input type="checkbox" name="tut[]" class="chk" id="tut_<?php echo $l++; ?>" value="<? echo $result->getId(); ?>/<? echo $result->getFile(); ?>"></td>
				</tr>			
	
<?php
		}
	}
	if($i==0)
	{
		echo "No tutorials.";
	}

}
	// Tutorials end.

	// Exam papers List start.
while($row=mysql_fetch_array($return_e))
{
	$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
	$row1=mysql_fetch_row($result1);
	if($row1[0]==null)
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=mysql_fetch_row($result1);			
	}
?>
		<tr class="heading">
			<td class="sub_code"><?echo $row[0] //Subject Code?></td>
			<td class="type"><!--Type--></td>
			<td class="delete"><!--Delete files--></td>
		</tr>
<?php
		$return_exam=database::getExamPaperObject("COURSE_ID",$row[0],null);
	$i=0;
	
	foreach($return_exam as $result)
	{
		if(($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses)) && $result->getFacultyId()==$facUsername)
		{
			$i++;


?>
				<tr class="list">
				<td><a href="<? echo EXAMDIR; ?>/<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>">
<?echo $result->getTopic(); ?></a></td>
<td>Exam Papers</td>
<td><input type="checkbox" name="exam[]" class="chk" id="lec_<?php echo $l++; ?>" value="<? echo $result->getId(); ?>/<? echo $result->getFile(); ?>"></td>
				</tr>			
	
<?php
		}
	}
	if($i==0)
	{
		echo "No exam papers.";
	}

}
	// Exam Papers end.

	// Solutions List start.
while($row=mysql_fetch_array($return_s))
{
	$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
	$row1=mysql_fetch_row($result1);
	if($row1[0]==null)
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=mysql_fetch_row($result1);			
	}
?>
		<tr class="heading">
			<td class="sub_code"><?echo $row[0] //Subject Code?></td>
			<td class="type"><!--Type--></td>
			<td class="delete"><!--Delete files--></td>
		</tr>
<?php
		$return_soln=database::getSolnObject("COURSE_ID",$row[0],null);
	$i=0;
	
	foreach($return_soln as $result)
	{
		if(($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses)) && $result->getFacultyId()==$facUsername)
		{
			$i++;


?>
				<tr class="list">
				<td><a href="<? echo SOLNDIR; ?>/<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>">
<?echo $result->getTopic(); ?></a></td>
<td>Solutions</td>
<td><input type="checkbox" name="soln[]" class="chk" id="lec_<?php echo $l++; ?>" value="<? echo $result->getId(); ?>/<? echo $result->getFile(); ?>"></td>
				</tr>			
	
<?php
		}
	}
	if($i==0)
	{
		echo "No solutions.";
	}

}
	// Solutions end.
?>
			<input type="submit" value="Delete selected">

			</form>
		</table>	
	</div>		
		
</div> </div>
		<div id="footer">
			<div id="footer_text">
			<div id="bottom_curve_lt">&nbsp;</div>
			<div id="img">Credits: <a href="http://www.iitr.ernet.in/campus_life/pages/Groups_and_Societies+IMG.html" target="_blank">Information Management Group</a></div>
			
			<div id="bottom_curve_rt">&nbsp;&nbsp;</div>
			</div>
		</div>
		<!--Footer ends here-->
<?php

database::closeDatabase();
?>


 <script type="text/javascript" src="/static/js/piwik.js"></script>
</body>
</html>
