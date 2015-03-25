<div class="ss" id="my_courses_goto">
	<div id="mcl_container"> <div id="mcl">	</div> 
		<a href="javascript:func1('#main_goto');"><div class="link_space"></div> </a>
		 <a href="javascript:func1('#browse_by_department_goto');"><div class="link_space"></div> </a>
	</div>
	<div id="mcr"></div>
	<div id="my_courses" >
		<div id="back_link_container_mc">
			<a href="javascript:func1('#main_goto');">
			<div  id="my_courses_back" >
				<div class="my_courses_back_link space" >back&nbsp;to&nbsp;main&nbsp;page</div>
			</div>
			</a>
			<a href="javascript:func1('#browse_by_department_goto');"> 
			<div id="my_courses_bbd_back">
				<div class="my_courses_bbd_back_link space" >upload</div>
			</div>
			</a>
		</div>
		<div id="my_courses_page_container">
			<div id="my_courses_topbar">
				<div id="my_courses_logout_button" >
<?php

if($_SESSION['user']=='s')
{
	header("Location: ../pages/final_student.php");
}
if($loggedIn==0)
{
	echo "<a href=\"index.php\">LOGIN</a>";
}
else
{
	echo "<a href=\"logout.php\">LOGOUT</a>";
database::connectToDatabase('facapp');
$facName=pg_fetch_array(database::executeQuery('facapp',database::getFacName($facId)));
database::closeDatabase('facapp');

?>
			</div>
			<div id="my_courses_title">MY COURSES</div>
			<div id="whats_new"><?echo "Welcome $facName[0]"; ?></div>
		</div>
		<div id="my_courses_selection">
			<a href="javascript:func2('_lectures','#my_courses_files','#my_courses_lectures_link');"  id="my_courses_lectures_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">LECTURES</a>
			<a href="javascript:func2('_tutorials','#my_courses_files','#my_courses_tutorials_link');"  id="my_courses_tutorials_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">TUTORIALS</a>
			<a href="javascript:func2('_exam_papers','#my_courses_files','#my_courses_exam_papers_link');"  id="my_courses_exam_papers_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">EXAM PAPERS</a>
			<a href="javascript:func2('_solutions','#my_courses_files','#my_courses_solutions_link');"  id="my_courses_solutions_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">SOLUTIONS</a>
		</div>

<?php
$temp=$_GET['temp2'];
if(isset($temp))
{
	if ($temp=='d')
		print("Files Deleted");
	else if ($temp=='nd')
		print("File not deleted. Please try later.");
	else
		print("File does not exist.");
}

database::connectToDatabase('intranet');

$return_lec=database::getLecObject("FACULTY_ID",$facId,null);
$return_tut=database::getTutObject("FACULTY_ID",$facId,null);
$return_exam=database::getExamPaperObject("FACULTY_ID",$facId,null);
$return_soln=database::getSolnObject("FACULTY_ID",$facId,null);

?>

<form name="delete" action="delete.php" method="post">
<?php

if(empty($return_lec) && empty($return_tut) && empty($return_exam) && empty($return_soln)) 
{
	echo "No files uploaded.";
}
else
{
if(!empty($return_lec))
{
?>
	<h3>Lectures</h3>
<?php
	$i=1;
	foreach($return_lec as $result)
	{
?>
	<tr>
		<td>
		<? echo $i++; ?>
		</td>
		<td>
		<a href="<? echo LECDIR."/$facId/".$result->getFile(); ?>"><? echo $result->getTopic(); ?></a>
		</td>	
		<td>
			<input type="checkbox" name="lec[]" value="<? echo $result->getId()."/".$result->getFile(); ?>">
		</td>
	</tr>
	<br>
<?
	}
}
if(!empty($return_tut))
{
?>
	<h3>Tutorials</h3>
<?php
	$i=1;
	foreach($return_tut as $result)
	{
?>
	<tr>
		<td>
		<? echo $i++; ?>
		</td>
		<td>
		<a href="<? echo TUTDIR."/$facId/".$result->getFile(); ?>"><? echo $result->getTopic(); ?></a>
		</td>
		<td>
			<input type="checkbox" name="tut[]" value="<? echo $result->getId()."/".$result->getFile(); ?>">
		</td>
	</tr>
	<br>
<?
	}
}
if(!empty($return_exam))
{
?>
	<h3>Exam Papers</h3>
<?php
	$i=1;
	foreach($return_exam as $result)
	{
?>
	<tr>
		<td>
		<? echo $i++; ?>
		</td>
		<td>
		<a href="<? echo EXAMDIR."/$facId/".$result->getFile(); ?>"><? echo $result->getTopic(); ?></a>
		</td>
		<td>
			<input type="checkbox" name="exam[]" value="<? echo $result->getId()."/".$result->getFile(); ?>">
		</td>
	</tr>
	<br>
<?
	}
}
if(!empty($return_soln))
{
?>
	<h3>Solutions</h3>
<?php
	$i=1;
	foreach($return_soln as $result)
	{
?>
	<tr>
		<td>
		<? echo $i++; ?>
		</td>
		<td>
		<a href="<? echo SOLNDIR."/$facId/".$result->getFile(); ?>"><? echo $result->getTopic(); ?></a>
		</td>
		<td>
			<input type="checkbox" name="soln[]" value="<? echo $result->getId()."/".$result->getFile(); ?>">
		</td>
	</tr>
	<br>
<?
	}
}
}

?>
<br>
<input type="submit" value="Delete">
</form>
<?
}
?>
		</div>
	</div>
</div>
<?php
database::closeDatabase('intranet');

?>

