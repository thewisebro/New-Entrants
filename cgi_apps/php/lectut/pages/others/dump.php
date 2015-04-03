<?php
session_start();

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
}

?>

<html>
	<head>
<?php		include_once("../common/styles.php"); ?>
	</head>
	<body>
		<div class="search_container" id="my_courses_goto">
			<div id="mcl_container"> 
				<div id="mcl">
				</div> 
				<a href="javascript:func1('#main_goto');"><div class="link_space"></div></a>
				<a href="javascript:func1('#browse_by_department_goto');"><div class="link_space"></div> </a>
			</div>
		<div id="mcr"></div>
		<div id="my_courses" >
			<div id="back_link_container_mc">
				<a href="index.php">
				<div  id="my_courses_back" >
					<div class="my_courses_back_link space" >back&nbsp;to&nbsp;main&nbsp;page</div>
				</div>
				</a>
				<a href="final_student.php"> 
				<div id="my_courses_bbd_back">
					<div class="my_courses_bbd_back_link space" >browse&nbsp;by&nbsp;department&nbsp;</div>
				</div>
				</a>
			</div>
			<div id="my_courses_page_container">
				<div id="my_courses_topbar">
					<div id="my_courses_logout_button" >
<?php
	if($loggedIn==0)
	{
		echo "<a href=\"index.php\">LOGIN</a>";
	}
	else
	{
		echo "<a href=\"logout.php\">LOGOUT</a>";
	}	
?>		
					</div>
					<div id="my_courses_title">SEARCH RESULTS</div>
					<div id="whats_new">
<?php

$search=filter_input(INPUT_GET,'search',FILTER_SANITIZE_STRING);
$search=secure($search);

$len=strlen($search);

if($len<2)
{
	echo "Search string should be atleast 3 characters long or department code.";
}
else
{

database::connectToDatabase("intranet");
database::connectToDatabase("regol");

if(isset($studId))
{
	$reg_courses=database::executeQuery('regol',database::studQuery($studId));
}
$time1=microtime(true);
$results_lec = search_perform($search,"lec");
$results_tut = search_perform($search,"tut");
$results_exam = search_perform($search,"exam");
$results_soln = search_perform($search,"soln");
$time2=microtime(true);
$time=$time2-$time1;
$time=round($time,3);
echo "<div id=\"whats_new\">$search ($time seconds)</div>";
?>

					</div>
				</div>
				<div id="my_courses_selection">
					<a href="javascript:func2('_lectures','#my_courses_files','#my_courses_lectures_link');"  id="my_courses_lectures_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">LECTURES</a>
					<a href="javascript:func2('_tutorials','#my_courses_files','#my_courses_tutorials_link');"  id="my_courses_tutorials_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">TUTORIALS</a>
					<a href="javascript:func2('_exam_papers','#my_courses_files','#my_courses_exam_papers_link');"  id="my_courses_exam_papers_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">EXAM PAPERS</a>
					<a href="javascript:func2('_solutions','#my_courses_files','#my_courses_solutions_link');"  id="my_courses_solutions_link" class="my_courses_selection_link my_courses_inactive_link my_courses_link">SOLUTIONS</a>
				</div>

<?php
	$courses=array();	
	$count=0;

	foreach($results_lec[$count] as $result)
	{
		if(!in_array($result->getCourseId(),$courses))
		{
			$prevCourse=$result->getCourseId();
			array_push($courses,$prevCourse);
			$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$prevCourse'"));
			$row1=pg_fetch_row($result1);
			if($row1[0]==null)
			{
				$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$prevCourse'"));
				$row1=pg_fetch_row($result1);			
			}
?>
			<a href="javascript:func3('<? echo $prevCourse; ?>','#my_courses_files','.<? echo $prevCourse; ?>');" id="<? echo $prevCourse; ?>" class="my_courses_course_link <? echo $prevCourse; ?>_link mc_course_link">
			<div id="<? echo $prevCourse; ?>" class="course_code"><? echo $prevCourse; ?></div>
			<div class="course_name"><? echo $row1[0]; ?></div>
			</a>
<?php
		}
	}
	foreach($results_tut[$count] as $result)
	{
		if(!in_array($result->getCourseId(),$courses))
		{
			$prevCourse=$result->getCourseId();
			array_push($courses,$prevCourse);
			$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$prevCourse'"));
			$row1=pg_fetch_row($result1);
			if($row1[0]==null)
			{
				$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$prevCourse'"));
				$row1=pg_fetch_row($result1);			
			}
?>
			<a href="javascript:func3('<? echo $prevCourse; ?>','#my_courses_files','.<? echo $prevCourse; ?>');" id="<? echo $prevCourse; ?>" class="my_courses_course_link <? echo $prevCourse; ?>_link mc_course_link">
			<div id="<? echo $prevCourse; ?>" class="course_code"><? echo $prevCourse; ?></div>
			<div class="course_name"><? echo $row1[0]; ?></div>
			</a>
<?php
		}
	}
	foreach($results_exam[$count] as $result)
	{
		if(!in_array($result->getCourseId(),$courses))
		{
			$prevCourse=$result->getCourseId();
			array_push($courses,$prevCourse);
			$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$prevCourse'"));
			$row1=pg_fetch_row($result1);
			if($row1[0]==null)
			{
				$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$prevCourse'"));
				$row1=pg_fetch_row($result1);			
			}
?>
			<a href="javascript:func3('<? echo $prevCourse; ?>','#my_courses_files','.<? echo $prevCourse; ?>');" id="<? echo $prevCourse; ?>" class="my_courses_course_link <? echo $prevCourse; ?>_link mc_course_link">
			<div id="<? echo $prevCourse; ?>" class="course_code"><? echo $prevCourse; ?></div>
			<div class="course_name"><? echo $row1[0]; ?></div>
			</a>
<?php
		}
	}
	foreach($results_soln[$count] as $result)
	{
		if(!in_array($result->getCourseId(),$courses))
		{
			$prevCourse=$result->getCourseId();
			array_push($courses,$prevCourse);
			$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$prevCourse'"));
			$row1=pg_fetch_row($result1);
			if($row1[0]==null)
			{
				$result1=database::executeQuery("regol",database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$prevCourse'"));
				$row1=pg_fetch_row($result1);			
			}
?>
			<a href="javascript:func3('<? echo $prevCourse; ?>','#my_courses_files','.<? echo $prevCourse; ?>');" id="<? echo $prevCourse; ?>" class="my_courses_course_link <? echo $prevCourse; ?>_link mc_course_link">
			<div id="<? echo $prevCourse; ?>" class="course_code"><? echo $prevCourse; ?></div>
			<div class="course_name"><? echo $row1[0]; ?></div>
			</a>
<?php
		}
	}

?>
<form name="download" action="download.php" method="post">
				<div id="scrollbarer">
					<div class="scrollbar"><div class="track"><div class="thumb"><div class="end"></div></div></div></div>
					<div class="viewport">
						 <div class="overview">
							<div id="my_courses_files">
								<div id="subjects" class="subjects">
<?php

foreach($courses as $row)
{
?>
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
		<td>	<a class="file list_selected <? echo $row; ?>" href="<? echo LECDIR; ?>/<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"><? echo $result->getTopic(); ?></a></td>
		<td>	<input type="checkbox" name="lec[]" value="<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"></td>
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
		<td>	<a class="file list_selected <? echo $row; ?>" href="<? echo TUTDIR; ?>/<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"><? echo $result->getTopic(); ?></a></td>
		<td>	<input type="checkbox" name="tut[]" value="<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"></td>
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
		<td>	<a class="file list_selected <? echo $row; ?>" href="<? echo EXAMDIR; ?>/<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"><? echo $result->getTopic(); ?></a></td>
		<td>	<input type="checkbox" name="exam[]" value="<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"></td>
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
		<td>	<a class="file list_selected <? echo $row; ?>" href="<? echo SOLNDIR; ?>/<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"><? echo $result->getTopic(); ?></a></td>
		<td>	<input type="checkbox" name="soln[]" value="<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"></td>
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
					</div>
<?
}
?>
				</div>
			</div>
		</div>
	</div>
<br>
<input type="submit" value="Download">
</form>
</div>
<a id="search_box_link" href="javascript:s();">
	<div id = "search_link">Search again</div>
</a>
</div>
</div>
</div>
<div class="search">
	<div href="#" class="close-meerkat">X</div>
<div id="search_box">
	<input type="text" id="search_input">
	<a id="search_submit" href="" >Search</a>
</div>
</div>
</body>
</html>
<?php

database::closeDatabase("regol");
database::closeDatabase("intranet");


?>
