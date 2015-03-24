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
				<div class="my_courses_bbd_back_link space" >browse&nbsp;by&nbsp;department&nbsp;</div>
			</div>
			</a>
		</div>
		<div id="my_courses_page_container">
			<div id="my_courses_topbar">
				<div id="my_courses_logout_button" >
<?php

if($_SESSION['user']=='f')
{
	header("Location: ../pages/final_prof.php");
}
if($loggedIn==0)
{
	echo "<a href=\"index.php\">LOGIN</a>";
}
else
{
	echo "<a href=\"logout.php\">LOGOUT</a>";

	
database::connectToDatabase('regol');

$studName=pg_fetch_array(database::executeQuery('regol',database::getStudName($studId)));
$reg_courses_l=database::executeQuery('regol',database::studQuery($studId));
$reg_courses_t=database::executeQuery('regol',database::studQuery($studId));
$reg_courses_e=database::executeQuery('regol',database::studQuery($studId));
$reg_courses_s=database::executeQuery('regol',database::studQuery($studId));

$Courses=array();
$CourseName=array();

while($row=pg_fetch_array($reg_courses_l))
{
	$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
	$row1=pg_fetch_row($result1);
	if($row1[0]==null)
	{
		$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=pg_fetch_row($result1);			
	}
	if(!in_array($row[1],$Courses))
	{
		array_push($Courses,$row[1]);
		array_push($CourseName,$row1[0]);
	}
}
while($row=pg_fetch_array($reg_courses_t))
{
	$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
	$row1=pg_fetch_row($result1);
	if($row1[0]==null)
	{
		$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=pg_fetch_row($result1);			
	}
	$return_lec=database::getTutObject("COURSE_ID",$row[0],null);
	if(!in_array($row[1],$Courses))
	{
		array_push($Courses,$row[1]);
		array_push($CourseName,$row1[0]);
	}
}
while($row=pg_fetch_array($reg_courses_e))
{
	$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
	$row1=pg_fetch_row($result1);
	if($row1[0]==null)
	{
		$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=pg_fetch_row($result1);			
	}
	if(!in_array($row[1],$Courses))
	{
		array_push($Courses,$row[1]);
		array_push($CourseName,$row1[0]);
	}
}
while($row=pg_fetch_array($reg_courses_s))
{
	$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
	$row1=pg_fetch_row($result1);
	if($row1[0]==null)
	{
		$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=pg_fetch_row($result1);			
	}
	if(!in_array($row[1],$Courses))
	{
		array_push($Courses,$row[1]);
		array_push($CourseName,$row1[0]);
	}
}

database::closeDatabase('regol');
database::connectToDatabase('intranet');

?>	
			</div>
			<div id="my_courses_title">MY COURSES</div>
			<div id="whats_new"><?echo "Welcome $studName[0]"; ?></div>
		</div>
		<div id="my_courses_selection">
			<a href="javascript:func2('_lectures','#my_courses_files','#my_courses_lectures_link');"  id="my_courses_lectures_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">LECTURES</a>
			<a href="javascript:func2('_tutorials','#my_courses_files','#my_courses_tutorials_link');"  id="my_courses_tutorials_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">TUTORIALS</a>
			<a href="javascript:func2('_exam_papers','#my_courses_files','#my_courses_exam_papers_link');"  id="my_courses_exam_papers_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">EXAM PAPERS</a>
			<a href="javascript:func2('_solutions','#my_courses_files','#my_courses_solutions_link');"  id="my_courses_solutions_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">SOLUTIONS</a>
		</div>
		<div id="my_courses_course_selection">
<?php
$i=0;
foreach($Courses as $sub)
{
?>
		<a href="javascript:func3('<? echo $sub; ?>','#my_courses_files','.<? echo $sub; ?>');" id="<? echo $sub; ?>" class="my_courses_course_link <? echo $sub; ?>_link mc_course_link">
		<div class="course_code"><? echo $sub; ?></div>
		<div class="course_name"><? echo $CourseName[$i]; ?></div>
		</a>
<?php
	$i++;
}
?>
	</div>
	<div id="scrollbarer">
		<div class="scrollbar"><div class="track"><div class="thumb"><div class="end"></div></div></div></div>
		<div class="viewport">
			 <div class="overview">
				<div id="my_courses_files">
					<div id="subjects" class="subjects">
<form name="download" action="download.php" method="post">

<?php

foreach($Courses as $row)
{
?>
<div id="<? echo $row; ?>">
	<div id="<? echo $row; ?>_lists">
		<div id="<? echo $row; ?>_lectures" class="file_list">
<?php
		$return_lec=database::getLecObject("COURSE_ID",$row,null);
	foreach($return_lec as $result)
	{
		if($result->getPermission()=='f' || in_array($result->getCourseId(),$reg_courses) || $facId==$id)
		{
?>
	<tr>
		<td><? echo $result->getFacultyId(); ?></td>						
		<td>	<a class="file list_selected <? echo $row; ?>" href="<? echo LECDIR; ?>/$id/<? echo $result->getFile(); ?>"><? echo $result->getTopic(); ?></a></td>
		<td>	<input type="checkbox" name="lec[]" value="<? echo $id; ?>/<? echo $result->getFile(); ?>"></td>
	</tr>
<?php
		}
	}
?>
		</div>
		<div id="<? echo $row; ?>_tutorials" class="file_list">
<?php
		$return_lec=database::getTutObject("COURSE_ID",$row[0],null);
	foreach($return_lec as $result)
	{
		if($result->getPermission()=='f' || in_array($result->getCourseId(),$reg_courses) || $facId==$id)
		{
?>
	<tr>
		<td><? echo $result->getFacultyId(); ?></td>						
		<td>	<a class="file list_selected <? echo $row; ?>" href="<? echo TUTDIR; ?>/$id/<? echo $result->getFile(); ?>"><? echo $result->getTopic(); ?></a></td>
		<td>	<input type="checkbox" name="tut[]" value="<? echo $id; ?>/<? echo $result->getFile(); ?>"></td>
	</tr>
<?php
		}
	}
?>
		</div>
		<div id="<? echo $row; ?>_exam_papers" class="file_list">
<?php
		$return_lec=database::getExamPaperObject("COURSE_ID",$row[0],null);
	foreach($return_lec as $result)
	{
		if($result->getPermission()=='f' || in_array($result->getCourseId(),$reg_courses) || $facId==$id)
		{
?>
	<tr>
		<td><? echo $result->getFacultyId(); ?></td>						
		<td>	<a class="file list_selected <? echo $row; ?>" href="<? echo EXAMDIR; ?>/$id/<? echo $result->getFile(); ?>"><? echo $result->getTopic(); ?></a></td>
		<td>	<input type="checkbox" name="exam[]" value="<? echo $id; ?>/<? echo $result->getFile(); ?>"></td>
	</tr>
<?php
		}
	}
?>
		</div>
		<div id="<? echo $row; ?>_solutions" class="file_list">
<?php
		$return_lec=database::getSolnObject("COURSE_ID",$row[0],null);
	foreach($return_lec as $result)
	{
		if($result->getPermission()=='f' || in_array($result->getCourseId(),$reg_courses) || $facId==$id)
		{
?>
	<tr>
		<td><? echo $result->getFacultyId(); ?></td>			
		<td>	<a class="file list_selected <? echo $row; ?>" href="<? echo SOLNDIR; ?>/$id/<? echo $result->getFile(); ?>"><? echo $result->getTopic(); ?></a></td>
		<td>	<input type="checkbox" name="soln[]" value="<? echo $id; ?>/<? echo $result->getFile(); ?>"></td>
	</tr>
<?php
		}
	}
?>
		</div>
	</div>
</div>
<?php
}
?>

<br>
<input type="submit" value="Download">
</form>
					</div>
<?
}
?>
				</div>
			</div>
		</div>
	</div>
</div>
<?
database::closeDatabase('intranet');

?>

