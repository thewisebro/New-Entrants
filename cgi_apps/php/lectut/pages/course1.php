<?php
include_once("../common/functions.php");
include("../../session/django_session.php");

$session = New Session();

if($_SESSION['group']=='s')	
	$studId=$_SESSION['lectut_userid'];
if($_SESSION['group']=='f')
	$facId=$_SESSION['lectut_userid'];

$id=$_GET['id'];
$name=$_GET['name'];
$facUsername=$_SESSION['lectut_username'];

database::connectToDatabase();
if(isset($studId))
{
	$reg_courses=database::executeQuery(database::studQuery($studId));
}
$result_l=database::executeQuery(database::getDistinctId(COURSE_ID,LEC_TABLE,"WHERE ".FACULTY_ID."='$id'"));
$result_t=database::executeQuery(database::getDistinctId(COURSE_ID,TUT_TABLE,"WHERE ".FACULTY_ID."='$id'"));
$result_e=database::executeQuery(database::getDistinctId(COURSE_ID,EXAM_TABLE,"WHERE ".FACULTY_ID."='$id'"));
$result_s=database::executeQuery(database::getDistinctId(COURSE_ID,SOLN_TABLE,"WHERE ".FACULTY_ID."='$id'"));
?>

<?php

$Courses=array();
$CourseName=array();
 
while($row=mysql_fetch_row($result_l))
{
	if($row[0]!="")
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=mysql_fetch_row($result1);
		/*if($row1[0]==null)
		{
			$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
			$row1=pg_fetch_row($result1);			
		}*/
		$return_lec=database::getLecObject("COURSE_ID",$row[0],null);

		foreach($return_lec as $result)
		{
			if($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses) || $facUsername==$id)
			{
				if(!in_array($result->getCourseId(),$Courses))
				{				
					array_push($Courses,$result->getCourseId());
					array_push($CourseName,$row1[0]);
				}
			}
		}
	}
}

while($row=mysql_fetch_row($result_t))
{
	if($row[0]!="")
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=mysql_fetch_row($result1);
		/*if($row1[0]==null)
		{
			$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
			$row1=pg_fetch_row($result1);			
		}*/
		$return_lec=database::getTutObject("COURSE_ID",$row[0],null);
		foreach($return_lec as $result)
		{
			if($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses) || $facUsername==$id)
			{
				if(!in_array($result->getCourseId(),$Courses))
				{
					array_push($Courses,$result->getCourseId());
					array_push($CourseName,$row1[0]);
				}
			}
		}
	}

}

while($row=mysql_fetch_row($result_e))
{
	if($row[0]!="")
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=mysql_fetch_row($result1);
	  /*if($row1[0]==null)
		{
			$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
			$row1=pg_fetch_row($result1);			
		}*/
		$return_lec=database::getExamPaperObject("COURSE_ID",$row[0],null);
		foreach($return_lec as $result)
		{
			if($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses) || $facUsername==$id)
			{
				if(!in_array($result->getCourseId(),$Courses))
				{
					array_push($Courses,$result->getCourseId());
					array_push($CourseName,$row1[0]);
				}		
			}
		}
	}	
}

while($row=mysql_fetch_row($result_s))
{
	if($row[0]!="")
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=mysql_fetch_row($result1);
		/*if($row1[0]==null)
		{
			$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
			$row1=pg_fetch_row($result1);			
		}*/
		$return_lec=database::getSolnObject("COURSE_ID",$row[0],null);
		foreach($return_lec as $result)
		{
			if($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses) || $facUsername==$id)
			{
				if(!in_array($result->getCourseId(),$Courses))
				{
					array_push($Courses,$result->getCourseId());
					array_push($CourseName,$row1[0]);
				}
			}
		}
	}
}
$i=0;
foreach($Courses as $CourseId)
{	
?>

	<a href="javascript:func32('<? echo $CourseId; ?>','#details_tab_container','.<? echo $CourseId; ?>','<? echo $id; ?>','<? echo $name; ?>','down');" id="<? echo$CourseId; ?>" class="browse_by_department_course_link <? echo $CourseId; ?>_link bbd_course_link">
	<div class="course_code"><? echo $CourseId; ?></div>
	<div class="course_name"><? echo $CourseName[$i]; ?></div>
	</a>
<?
	$i++;
}

database::closeDatabase();
?>

