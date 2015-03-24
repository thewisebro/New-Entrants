<?php
include_once("../common/functions.php");
include_once("../commom/constants.php");

?>

<div class="ss" id="my_courses_goto">
	<div id="mcl_container"> <div id="mcl">	</div> 
		<!--[if !(IE 6)]><!-->
				<a href=\"javascript:func1('#main_goto');\">
		<!--<![endif]-->
		<!--[if IE 6]>
				<a href=\"javascript:ie_func1('#main_goto')\">
		<![endif]-->
		<div class="link_space"></div> </a>
   		<!--[if !(IE 6)]><!-->
				<a href=\"javascript:func1('#browse_by_department_goto');\">
		<!--<![endif]-->
		<!--[if IE 6]>
				<a href=\"javascript:ie_func1('#browse_by_department_goto')\">
		<![endif]-->
		<div class="link_space"></div> </a>
	</div>
	<div id="mcr"></div>
	<div id="my_courses" >
		<div id="back_link_container_mc">
			<!--[if !(IE 6)]><!-->
			<a href="javascript:func1('#main_goto');">
			<!--<![endif]-->
			<!--[if IE 6]>
			<a href="javascript:ie_func1('#main_goto');">
			<![endif]-->
			<div  id="my_courses_back" >
				<div class="my_courses_back_link space" >back&nbsp;to&nbsp;main&nbsp;page</div>
			</div>
			</a>
			<!--[if !(IE 6)]><!-->
			<a href="javascript:func1('#browse_by_department_goto');">
			<!--<![endif]-->
			<!--[if IE 6]>
			<a href="javascript:ie_func1('#browse_by_department_goto');">
			<![endif]-->
			<div id="my_courses_bbd_back">
				<div class="my_courses_bbd_back_link space" >browse&nbsp;by&nbsp;department&nbsp;</div>
			</div>
			</a>
		</div>
		<div id="my_courses_page_container">
		<form name="download" action="download.php" method="post" onsubmit="return validate_form();">
			<div id="my_courses_topbar">
					<div id="my_courses_logout_button" >
<?php

if($_SESSION['group']=='f')
{
	header("Location: ../pages/final_prof.php");
}
if(!$loggedIn)
{
	echo "<a href=\"index.php\">LOGIN</a>";
}
else
{
	echo "<a href=\"/nucleus/logout\">LOGOUT</a>";

	
database::connectToDatabase();

$studName=mysql_fetch_array(database::executeQuery(database::getStudName($studId)));
$reg_courses_l=database::executeQuery(database::studQuery($studId));
$reg_courses_t=database::executeQuery(database::studQuery($studId));
$reg_courses_e=database::executeQuery(database::studQuery($studId));
$reg_courses_s=database::executeQuery(database::studQuery($studId));

$Courses=array();
$CourseName=array();
while($row=mysql_fetch_array($reg_courses_l))
{
	$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[1]'"));
  $row1=mysql_fetch_row($result1);
	/*if($row1[0]==null)
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[1]'"));
		$row1=mysql_fetch_row($result1);			
	}*/
	if(!in_array($row[1],$Courses))
	{
		array_push($Courses,$row[1]);
		array_push($CourseName,$row1[0]);
	}
}
while($row=mysql_fetch_array($reg_courses_t))
{
	$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[1]'"));
	$row1=mysql_fetch_row($result1);
	/*if($row1[0]==null)
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[1]'"));
		$row1=mysql_fetch_row($result1);			
	}*/
	$return_lec=database::getTutObject("COURSE_ID",$row[0],null);
	if(!in_array($row[1],$Courses))
	{
		array_push($Courses,$row[1]);
		array_push($CourseName,$row1[0]);
	}
}
while($row=mysql_fetch_array($reg_courses_e))
{
	$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[1]'"));
	$row1=mysql_fetch_row($result1);
	/*if($row1[0]==null)
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[1]'"));
		$row1=mysql_fetch_row($result1);			
	}*/
	if(!in_array($row[1],$Courses))
	{
		array_push($Courses,$row[1]);
		array_push($CourseName,$row1[0]);
	}
}
while($row=mysql_fetch_array($reg_courses_s))
{
	$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[1]'"));
	$row1=mysql_fetch_row($result1);
	/*if($row1[0]==null)
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[1]'"));
		$row1=mysql_fetch_row($result1);			
	}*/
	if(!in_array($row[1],$Courses))
	{
		array_push($Courses,$row[1]);
		array_push($CourseName,$row1[0]);
	}
}
}
?>	
				</div>
				<div id="my_courses_title">MY COURSES</div>
				<div id="welcome_text"><?echo "Welcome $studName[0]"; ?></div>
			</div>
			<div id="my_courses_selection">
				<a href="javascript:func2('_lectures','#my_courses_files','#my_courses_lectures_link');"  id="my_courses_lectures_link" 	class="my_courses_selection_link my_courses_inactive_link my_courses_link">LECTURES</a>
				<a href="javascript:func2('_tutorials','#my_courses_files','#my_courses_tutorials_link');"  id="my_courses_tutorials_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">TUTORIALS</a>
				<a href="javascript:func2('_exam_papers','#my_courses_files','#my_courses_exam_papers_link');"  id="my_courses_exam_papers_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">EXAM PAPERS</a>
				<a href="javascript:func2('_solutions','#my_courses_files','#my_courses_solutions_link');"  id="my_courses_solutions_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">SOLUTIONS</a>
				<a href="javascript:func2('_all','#my_courses_files','#my_courses_all_link');"  id="my_courses_all_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">ALL</a>
			</div>
			


			<div id="my_courses_course_selection">
			<div class="scrollbarer">
					
					<div class="scrollbar"><div class="track"><div class="thumb"><div class="end"></div></div></div></div>
<!-- this set and not overview as this is the relatively outermost container div  -->
				<div class="viewport" id="scroll_dept_target">
			 <div class="overview" style="height:auto;">
<?php
$i=0;
foreach($Courses as $CourseId)
{	
?>

	<a href="javascript:func321('<? echo $CourseId; ?>','#details_tab_container','.<? echo $CourseId; ?>');" id="<? echo$CourseId; ?>" class="my_courses_course_link <? echo $CourseId; ?>_link bbd_course_link">
	<div class="course_code"><? echo $CourseId; ?></div>
	<div class="course_name"><? echo $CourseName[$i]; ?></div>
	<a>
<?
	$i++;
}
?>
			</div>
			</div></div></div>
			<div id="scrollbarer">
				<div class="scrollbarer">
				<div class="scrollbar"><div class="track"><div class="thumb"><div class="end"></div></div></div></div>
				<div class="viewport">
					 <div class="overview">
						<div id="my_courses_files">
              
							<div id="subjects_reg" class="subjects"> <img id="loading"  style="display:none" src="../styles/ajax-loader.gif"/>
              </div>
						</div>
					</div>
				</div>
				</div>
			</div>
			<br>
			<div style="margin-top:20px;">
			<input type="submit" value="Download selected" class="download_button" id="d_button_mc">
			<a id="search_box_link_" href="javascript:s();">
				<div id = "search_link_main">Search</div>
			</a>
			</div>
			</form>
		
			


		


		</div>
	</div>
				
</div>
<?
database::closeDatabase();

?>

