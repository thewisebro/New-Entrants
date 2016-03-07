<?php

//session_start();

//to not allow students to login
header("Location: ../pages/index.php");
/*
include_once("../common/functions.php");

if(isLogin($_SESSION['username'],$_SESSION['sessionid']))
{
	if($_SESSION['user']=='s')	
		$studId=$_SESSION['username'];
	if($_SESSION['user']=='f')
		$facId=$_SESSION['username'];
	$loggedIn=1;
}
else
{
	$loggedIn=0;
	header("Location: logout.php");
}

if($loggedIn!=0 && $_SESSION['user']=='f')
{
	header("Location: faculty.php");
}

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

		<table id="file_list">
		<form name="download" action="download.php" method="post" onsubmit="return validate_form();">

		<?
database::connectToDatabase('regol');
database::connectToDatabase('intranet');
database::connectToDatabase("facapp");

$studName=pg_fetch_array(database::executeQuery('regol',database::getStudName($studId)));
$reg_courses_l=database::executeQuery('regol',database::studQuery($studId));
$reg_courses_t=database::executeQuery('regol',database::studQuery($studId));
$reg_courses_e=database::executeQuery('regol',database::studQuery($studId));
$reg_courses_s=database::executeQuery('regol',database::studQuery($studId));

$l=1;
$t=1;
$e=1;
$s=1;

	// Lectures List start.
while($row=pg_fetch_array($return_l))
{
	$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
	$row1=pg_fetch_row($result1);
	if($row1[0]==null)
	{
		$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=pg_fetch_row($result1);			
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
		if(($result->getPermission()=='f' || in_array($result->getCourseId(),$reg_courses)) && $result->getFacultyId()==$facId)
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
while($row=pg_fetch_array($return_t))
{
	$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
	$row1=pg_fetch_row($result1);
	if($row1[0]==null)
	{
		$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=pg_fetch_row($result1);			
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
		if(($result->getPermission()=='f' || in_array($result->getCourseId(),$reg_courses)) && $result->getFacultyId()==$facId)
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
while($row=pg_fetch_array($return_e))
{
	$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
	$row1=pg_fetch_row($result1);
	if($row1[0]==null)
	{
		$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=pg_fetch_row($result1);			
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
		if(($result->getPermission()=='f' || in_array($result->getCourseId(),$reg_courses)) && $result->getFacultyId()==$facId)
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
while($row=pg_fetch_array($return_s))
{
	$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
	$row1=pg_fetch_row($result1);
	if($row1[0]==null)
	{
		$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=pg_fetch_row($result1);			
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
		if(($result->getPermission()=='f' || in_array($result->getCourseId(),$reg_courses)) && $result->getFacultyId()==$facId)
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

database::closeDatabase("facapp");
database::closeDatabase("intranet");
database::closeDatabase("regol");
?>


</body>
</html>

<?php
*/
?>
