<?php

include_once("../common/functions.php");

?>
<div class="ss" id="my_courses_goto">
	<div id="mcl_container"><div id="mcl">	</div> 
		<a href="javascript:func1('#main_goto');"><div class="link_space"></div> </a>
		<a href="javascript:func1('#browse_by_department_goto');"><div class="link_space"></div> </a>
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
				<div class="my_courses_bbd_back_link space" >upload</div>
			</div>
			</a>
		</div>
		<div id="my_courses_page_container">
			<form name="delete" action="delete.php" method="post" onsubmit="return validate_form();">
			<div id="my_courses_topbar">
				<div id="my_courses_logout_button" >
<?php

if($_SESSION['group']=='s')
{
	header("Location: ../pages/final_student.php");
}
if(!$loggedIn)
{
	echo "<a href=\"index.php\">LOGIN</a>";
}
else
{
	echo "<a href=\"/nucleus/logout\">LOGOUT</a>";
database::connectToDatabase();
$facName=mysql_fetch_array(database::executeQuery(database::getFacName($facId)));
$facUsername=$_SESSION['lectut_username'];

$return_lec=database::executeQuery(database::getDistinctId(COURSE_ID,LEC_TABLE,"WHERE ".FACULTY_ID."='$facUsername'"));
$return_tut=database::executeQuery(database::getDistinctId(COURSE_ID,TUT_TABLE,"WHERE ".FACULTY_ID."='$facUsername'"));
$return_exam=database::executeQuery(database::getDistinctId(COURSE_ID,EXAM_TABLE,"WHERE ".FACULTY_ID."='$facUsername'"));
$return_soln=database::executeQuery(database::getDistinctId(COURSE_ID,SOLN_TABLE,"WHERE ".FACULTY_ID."='$facUsername'"));

$Courses=array();
$CourseName=array();

while($row=mysql_fetch_array($return_lec))
{
	$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
  $row1=mysql_fetch_row($result1);
/*	if($row1[0]==null)
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=mysql_fetch_row($result1);			
	}*/
	if(!in_array($row[0],$Courses))
	{
		array_push($Courses,$row[0]);
		array_push($CourseName,$row1[0]);
	}
}
while($row=mysql_fetch_array($return_tut))
{
	$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
	$row1=mysql_fetch_row($result1);
	/*if($row1[0]==null)
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=mysql_fetch_row($result1);			
	}*/
	$return_lec=database::getTutObject("COURSE_ID",$row[0],null);
	if(!in_array($row[0],$Courses))
	{
		array_push($Courses,$row[0]);
		array_push($CourseName,$row1[0]);
	}
}
while($row=mysql_fetch_array($return_exam))
{
	$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
	$row1=mysql_fetch_row($result1);
	/*if($row1[0]==null)
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=mysql_fetch_row($result1);			
	}*/
	if(!in_array($row[0],$Courses))
	{
		array_push($Courses,$row[0]);
		array_push($CourseName,$row1[0]);
	}
}
while($row=mysql_fetch_array($return_soln))
{
	$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
	$row1=mysql_fetch_row($result1);
	/*if($row1[0]==null)
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=mysql_fetch_row($result1);			
	}*/
	if(!in_array($row[0],$Courses))
	{
		array_push($Courses,$row[0]);
		array_push($CourseName,$row1[0]);
	}
}
}
database::closeDatabase();

?>
				</div>
				<div id="my_courses_title">MY COURSES</div>
				<div id="welcome_text"><?echo "Welcome $facName[0]"; ?></div>
			</div>
			<div id="my_courses_selection">
				<a href="javascript:func2('_lectures','#my_courses_files','#my_courses_lectures_link');"  id="my_courses_lectures_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">LECTURES</a>
				<a href="javascript:func2('_tutorials','#my_courses_files','#my_courses_tutorials_link');"  id="my_courses_tutorials_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">TUTORIALS</a>
				<a href="javascript:func2('_exam_papers','#my_courses_files','#my_courses_exam_papers_link');"  id="my_courses_exam_papers_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">EXAM PAPERS</a>
				<a href="javascript:func2('_solutions','#my_courses_files','#my_courses_solutions_link');"  id="my_courses_solutions_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">SOLUTIONS</a>
				<a href="javascript:func2('_all','#my_courses_files','#my_courses_all_link');"  id="my_courses_all_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">ALL</a>
			</div>
<?php
$temp2=$_GET['temp2'];
echo "<div id='warning_managefiles' style='font-size:16px; color:#B00;'>";
if(isset($temp2))
{
/*	if ($temp2=='d')
		print("Files Deleted");
	else if ($temp2=='nd')
		print("Files not deleted. Please try later.");
	else if ($temp2=='b')
		print("");
	else
		print("Files do not exist.");
*/
	$logfile=fopen("../lectut_profs_logs.txt",'a');
	$logstring="";

	$d=$_GET['d'];
	$nd=$_GET['nd'];
	$ne=$_GET['ne'];
	if($d>0)
		echo "<script>$('#warning_managefiles').css('color','green');</script>$d files deleted.<br>";
	if($nd>0)
		echo "<script>$('#warning_managefiles').css('color','red');</script>$nd files not deleted. Please try again later.<br>";
	if($ne>0)
		echo "<script>$('#warning_maangefiles').css('color','red');</script>$ne files donot exist.<br>";

	$logstring=date("D F d Y",time())." ".$facUsername." $d files deleted. $nd files not deleted. Please try again later. $ne files donot exist.\n"; 	
	fwrite($logfile,$logstring);
	fclose($logfile);
}
echo "</div>";
?>
			<div id="my_courses_course_selection">
			<div class="scrollbarer">
					
					<div class="scrollbar"><div class="track"><div class="thumb"><div class="end"></div></div></div></div>
<!-- this set and not overview as this is the relatively outermost container div  -->
				<div class="viewport" id="scroll_dept_target">
			 <div class="overview" >
<?php
$i=0;
foreach($Courses as $CourseId)
{	
?>

			<a href="javascript:func32('<? echo $CourseId; ?>','#details_tab_container','.<? echo $CourseId; ?>','<? echo $facUsername; ?>','<? echo $facName[0]; ?>','del');" id="<? echo $CourseId; ?>" class="my_courses_course_link <? echo $CourseId; ?>_link">
			<div class="course_code"><? echo $CourseId; ?></div>
			<div class="course_name"><? echo $CourseName[$i]; ?></div>
			</a>
<?
	$i++;
}
?>
			</div>
			</div></div></div>
					<div id="scrollbarer">
					<div class="scrollbarer">
					
					<div class="scrollbar"><div class="track"><div class="thumb"><div class="end"></div></div></div></div>
<!-- this set and not overview as this is the relatively outermost container div  -->
				<div class="viewport" id="scroll_dept_target" style="width:410px;height:340px;">
			 <div class="overview" >
						<div id="my_courses_files">
							<div id="subjects" class="subjects"></div>
						</div>
					</div>
				</div>
			</div>
			</div>
			<div style="margin-top:20px;">
			<input type="submit" value="Delete selected" class="download_button" id="d_button_mc">
			<a id="search_box_link_" href="javascript:s();">
				<div id = "search_link_main">Search</div>
			</a>
			</div>

			</form>
		</div>
	</div>
</div>

