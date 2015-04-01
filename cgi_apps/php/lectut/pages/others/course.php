<?php

session_start();

include_once("../common/functions.php");

if(isLogin($_SESSION['username'],$_SESSION['sessionid']))
{
	if($_SESSION['user']=='s')	
		$studId=$_SESSION['username'];
	if($_SESSION['user']=='f')
		$facId=$_SESSION['username'];
}

$id=$_GET['id'];
$name=$_GET['name'];

database::connectToDatabase("intranet");
database::connectToDatabase("regol");
if(isset($studId))
{
	$reg_courses=database::executeQuery('regol',database::studQuery($studId));
}
$result_l=database::executeQuery("intranet",database::getDistinctId(COURSE_ID,LEC_TABLE,"WHERE ".FACULTY_ID."='$id'"));
$result_t=database::executeQuery("intranet",database::getDistinctId(COURSE_ID,TUT_TABLE,"WHERE ".FACULTY_ID."='$id'"));
$result_e=database::executeQuery("intranet",database::getDistinctId(COURSE_ID,EXAM_TABLE,"WHERE ".FACULTY_ID."='$id'"));
$result_s=database::executeQuery("intranet",database::getDistinctId(COURSE_ID,SOLN_TABLE,"WHERE ".FACULTY_ID."='$id'"));
$i=0;
?>

<form name="download" action="download.php" method="post">

<h3>Lectures</h3>
<table>

<?php

while($row=pg_fetch_row($result_l))
{
	if($row[0]!="")
	{
		$i++;
		$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=pg_fetch_row($result1);
		if($row1[0]==null)
		{
			$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
			$row1=pg_fetch_row($result1);			
		}
		$return_lec=database::getLecObject("COURSE_ID",$row[0],null);
?>

<tr>
	<td><? echo $i; ?></td>
	<td><? echo $row[0]."-".$row1[0]; ?>
</tr>
<tr>
<td></td>
<ul>
<?php
	$count=0;
	foreach($return_lec as $result)
	{
		if($result->getPermission()=='f' || in_array($result->getCourseId(),$reg_courses) || $facId==$id)
		{
			$count++;
?>		
		<td>
		<li>
		<a href="<? echo LECDIR."/$id/".$result->getFile(); ?>"><? echo $result->getTopic(); ?></a>
		</li></td>
		<td>
		<input type="checkbox" name="lec[]" value="<? echo $id."/".$result->getFile(); ?>">
		</td>
<?php
		}
	}
	if($count==0)
	{
		echo "No authorized lectures.";
	}
}
?>
</ul>
</tr>
<?	
}
if($i==0)
{
	echo "No lectures uploaded.";
}
?>
</table>
<?php
$i=0;
?>

<h3>Tutorials</h3>
<table>

<?php

while($row=pg_fetch_row($result_t))
{
	if($row[0]!="")
	{
		$i++;
		$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=pg_fetch_row($result1);
		if($row1[0]==null)
		{
			$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
			$row1=pg_fetch_row($result1);			
		}
		$return_lec=database::getTutObject("COURSE_ID",$row[0],null);
?>

<tr>
	<td><? echo $i; ?></td>
	<td><? echo $row[0]."-".$row1[0]; ?>
</tr>
<tr>
<td></td>
<ul>
<?php
	$count=0;
	foreach($return_lec as $result)
	{
		if($result->getPermission()=='f' || in_array($result->getCourseId(),$reg_courses) || $facId==$id)
		{
			$count++;
?>			
			<td>
			<li>
			<a href="<? echo TUTDIR."/$id/".$result->getFile(); ?>"><? echo $result->getTopic(); ?></a>
			</li></td>
			<td>
			<input type="checkbox" name="tut[]" value="<? echo $id."/".$result->getFile(); ?>">
			</td>
<?php
		}
	}
	if($count==0)
	{
		echo "No authorized tutorials.";
	}
?>
</ul>
</tr>
<?	
	}
}
if($i==0)
{
	echo "No tutorials uploaded.";
}
?>
</table>
<?php
$i=0;
?>

<h3>Exam Papers</h3>
<table>

<?php

while($row=pg_fetch_row($result_e))
{
	if($row[0]!="")
	{
		$i++;
		$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=pg_fetch_row($result1);
		if($row1[0]==null)
		{
			$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
			$row1=pg_fetch_row($result1);			
		}
		$return_lec=database::getExamPaperObject("COURSE_ID",$row[0],null);
?>

<tr>
	<td><? echo $i; ?></td>
	<td><? echo $row[0]."-".$row1[0]; ?>
</tr>
<tr>
<td></td>
<ul>
<?php
	$count=0;
	foreach($return_lec as $result)
	{
		if($result->getPermission()=='f' || in_array($result->getCourseId(),$reg_courses) || $facId==$id)
		{
			$count++;
?>			
			<td>
			<li>
			<a href="<? echo EXAMDIR."/$id/".$result->getFile(); ?>"><? echo $result->getTopic(); ?></a>
			</li></td>
			<td>
			<input type="checkbox" name="exam[]" value="<? echo $id."/".$result->getFile(); ?>">
			</td>
<?php
		}
	}
	if($count==0)
	{
		echo "No authorized exam papers.";
	}
?>
</ul>
</tr>
<?	
	}
}
if($i==0)
{
	echo "No exam papers uploaded.";
}
?>
</table>
<?php
$i=0;
?>

<h3>Solutions</h3>
<table>

<?php

while($row=pg_fetch_row($result_s))
{
	if($row[0]!="")
	{
		$i++;
		$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=pg_fetch_row($result1);
		if($row1[0]==null)
		{
			$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
			$row1=pg_fetch_row($result1);			
		}
		$return_lec=database::getSolnObject("COURSE_ID",$row[0],null);
?>

<tr>
	<td><? echo $i; ?></td>
	<td><? echo $row[0]."-".$row1[0]; ?>
</tr>
<tr>
<td></td>
<ul>
<?php
	$count=0;
	foreach($return_lec as $result)
	{
		if($result->getPermission()=='f' || in_array($result->getCourseId(),$reg_courses) || $facId==$id)
		{
			$count++;
?>			
			<td>
			<li>
			<a href="<? echo SOLNDIR."/$id/".$result->getFile(); ?>"><? echo $result->getTopic(); ?></a>
			</li></td>
			<td>
			<input type="checkbox" name="soln[]" value="<? echo $id."/".$result->getFile(); ?>">
			</td>

<?php
		}
	}
	if($count==0)
	{
		echo "No authorized solutions.";
	}
?>
</ul>
</tr>
<?	
	}
}
if($i==0)
{
	echo "No solutions uploaded.";
}
?>
</table>
<input type="submit" value="Download">
</form>
<?php

database::closeDatabase("intranet");
database::closeDatabase("regol");
?>

