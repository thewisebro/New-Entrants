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
$courseId=$_GET['course'];
$facUsername=$_SESSION['lectut_username'];


database::connectToDatabase();
if(isset($studId))
{
	$reg_courses=database::executeQuery(database::studQuery($studId));
}

$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$courseId'"));
$row1=mysql_fetch_row($result1);
if($row1[0]==null)
{
	$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$courseId'"));
	$row1=mysql_fetch_row($result1);			
}

$l=1;
$t=1;
$e=1;
$s=1;
?>
<div id="<? echo $courseId; ?>">
	<div id="<? echo $courseId; ?>_lists">
	<div id="<? echo $courseId; ?>_lectures" class="file_list">
	<div class="select_all_checkbox"><input type="checkbox" class="select_all" id="checkL"  onclick="select_all(this.id,'<? echo $courseId;?>_lectures');"><span style="float:right;">SELECT ALL</span></div>

<?php
		$return_lec=database::getLecObject("COURSE_ID",$courseId,null);
		$i=0;
	foreach($return_lec as $result)
	{
		if(($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses) || $facUsername==$id) && $result->getFacultyId()==$id)
		{
			$i++;
?>
			<div class="link_container"><a class="file list_selected <? echo $courseId; ?>" target="_blank" href="<? echo LECDIR; ?>/<? echo $id; ?>/<? echo $result->getFile(); ?>"><? echo $result->getTopic(); ?></a><input type="checkbox" name="lec[]" class="chk" id="lec_<?php echo $l++; ?>" value="<? echo $id; ?>/<? echo $result->getFile(); ?>"></div>
<?php
		}
	}
	if($i==0)
	{
		echo "No lectures.";
	}
?>
		</div>
		<div id="<? echo $courseId; ?>_tutorials" class="file_list">
		<div class="select_all_checkbox"><input type="checkbox" class="select_all" id="checkT"  onclick="select_all(this.id,'<? echo $courseId;?>_tutorials');"><span style="float:right;">SELECT ALL</span></div>

<?php

		$return_tut=database::getTutObject("COURSE_ID",$courseId,null);
	$i=0;
	foreach($return_tut as $result)
	{	
		if(($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses) || $facUsername==$id) && $result->getFacultyId()==$id)
		{
			$i++;
?>
			<div class="link_container"><a class="file list_selected <? echo $courseId; ?>" target="_blank"  href="<? echo TUTDIR; ?>/<? echo $id; ?>/<? echo $result->getFile(); ?>"><? echo $result->getTopic(); ?></a>
			<input type="checkbox" name="tut[]" class="chk"  id="tut_<? echo $t++; ?>" value="<? echo $id; ?>/<? echo $result->getFile(); ?>"></div>
<?php
		}
	}	
	if($i==0)
	{
		echo "No tutorials.";
	}

?>
		</div>
		<div id="<? echo $courseId; ?>_exam_papers" class="file_list">
		<div class="select_all_checkbox"><input type="checkbox" class="select_all" id="checkE"  onclick="select_all(this.id,'<? echo $courseId;?>_exam_papers');"><span style="float:right;">SELECT ALL</span></div>

<?php

		$return_exam=database::getExamPaperObject("COURSE_ID",$courseId,null);
	$i=0;
	foreach($return_exam as $result)
	{	
		if(($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses) || $facUsername==$id) && $result->getFacultyId()==$id)
		{
			$i++;
?>
			<div class="link_container"><a class="file list_selected <? echo $courseId; ?>" target="_blank"  href="<? echo EXAMDIR; ?>/<? echo $id; ?>/<? echo $result->getFile(); ?>"><? echo $result->getTopic(); ?></a>
			<input type="checkbox" name="exam[]" class="chk"  id="exam_<? echo $e++; ?>"value="<? echo $id; ?>/<? echo $result->getFile(); ?>"></div>
<?php
		}
	}	
	if($i==0)
	{
		echo "No exam papers.";
	}

?>
		</div>
		<div id="<? echo $courseId; ?>_solutions" class="file_list">
		<div class="select_all_checkbox"><input type="checkbox" class="select_all" id="checkS"  onclick="select_all(this.id,'<? echo $courseId;?>_solutions');"><span style="float:right;">SELECT ALL</span></div>

<?php
		$return_soln=database::getSolnObject("COURSE_ID",$courseId,null);
	$i=0;
	foreach($return_soln as $result)
	{	
		if(($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses) || $facUsername==$id) && $result->getFacultyId()==$id)
		{
			$i++;
?>
			<div class="link_container"><a class="file list_selected <? echo $courseId; ?>" target="_blank"  href="<? echo SOLNDIR; ?>/<? echo$id; ?>/<? echo $result->getFile(); ?>"><? echo $result->getTopic(); ?></a>
			<input type="checkbox" name="soln[]" class="chk"  id="soln_<? echo $s++; ?>" value="<? echo $id; ?>/<? echo $result->getFile(); ?>"></div>
<?php
		}
	}
	if($i==0)
	{
		echo "No solutions.";
	}

?>
		</div>
		<div id="<? echo $courseId; ?>_all" class="file_list">
		<div class="select_all_checkbox"><input type="checkbox" class="select_all" id="checkA"  onclick="select_all(this.id,'<? echo $courseId;?>_all');"><span style="float:right;">SELECT ALL</span></div>

<?php
	$i=0;
	echo "<div class='file_list' id='lec_all' style='width:100%; font-size:18px'>Lectures</div>";
	foreach($return_lec as $result)
	{
		if(($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses) || $facUsername==$id) && $result->getFacultyId()==$id)
		{
			$i++;
?>
			<div class="link_container"><a class="file list_selected <? echo $courseId; ?>" target="_blank"  href="<? echo LECDIR; ?>/<? echo $id; ?>/<? echo $result->getFile(); ?>"><? echo $result->getTopic(); ?></a>
			<input type="checkbox" name="lec[]" class="chk_all" id="lec_<?php echo $l++; ?>" value="<? echo $id; ?>/<? echo $result->getFile(); ?>"></div>
<?php
		}
	}
	if($i==0)
	{
		echo "<div class='file_list' id='exam_all' style='width:100%;text-align:center;'>No Lectures</div>";
	}
	echo "<br>";
	$i=0;
	echo "<div class='file_list' id='tut_all' style='width:100%; font-size:18px'>Tutorials</div>";
	foreach($return_tut as $result)
	{	
		if(($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses) || $facUsername==$id) && $result->getFacultyId()==$id)
		{
			$i++;
?>
			<div class="link_container"><a class="file list_selected <? echo $courseId; ?>" target="_blank"  href="<? echo TUTDIR; ?>/<? echo $id; ?>/<? echo $result->getFile(); ?>"><? echo $result->getTopic(); ?></a>
			<input type="checkbox" name="tut[]" class="chk_all"  id="tut_<? echo $t++; ?>" value="<? echo $id; ?>/<? echo $result->getFile(); ?>"></div>
<?php
		}
	}	
	if($i==0)
	{
		echo "<div class='file_list' id='exam_all' style='width:100%;text-align:center;'>No Tutorials</div>";
	}
	echo "<br>";
	$i=0;
	echo "<div class='file_list' id='exam_all' style='width:100%; font-size:18px;'>Exam Papers</div>";
	foreach($return_exam as $result)
	{	
		if(($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses) || $facUsername==$id) && $result->getFacultyId()==$id)
		{
			$i++;
?>
			<div class="link_container"><a class="file list_selected <? echo $courseId; ?>" target="_blank"  href="<? echo EXAMDIR; ?>/<? echo $id; ?>/<? echo $result->getFile(); ?>"><? echo $result->getTopic(); ?></a>
			<input type="checkbox" name="exam[]" class="chk_all"  id="exam_<? echo $e++; ?>"value="<? echo $id; ?>/<? echo $result->getFile(); ?>"></div>
<?php
		}
	}	
	if($i==0)
	{
		echo "<div class='file_list' id='exam_all' style='width:100%;text-align:center;'>No Exam Papers</div>";
	}
	echo "<br>";
	$i=0;
	echo "<div class='file_list' id='soln_all' style='width:100%; font-size:18px'>Solutions</div>";
	foreach($return_soln as $result)
	{	
		if(($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses) || $facUsername==$id) && $result->getFacultyId()==$id)
		{
			$i++;
?>
			<div class="link_container"><a class="file list_selected <? echo $courseId; ?>" target="_blank"  href="<? echo SOLNDIR; ?>/<? echo$id; ?>/<? echo $result->getFile(); ?>"><? echo $result->getTopic(); ?></a>
			<input type="checkbox" name="soln[]" class="chk_all"  id="soln_<? echo $s++; ?>" value="<? echo $id; ?>/<? echo $result->getFile(); ?>"></div>
<?php
		}
	}
	if($i==0)
	{
		echo "<div class='file_list' id='exam_all' style='width:100%; text-align:center;'>No Solutions</div>";
	}

?>
		</div>

	</div>
</div>
<?php

database::closeDatabase();
?>

