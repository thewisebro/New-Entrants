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
	if($_SESSION['group']=='f')
		$facId=$_SESSION['lectut_userid'];
	$loggedIn=true;
}
else
{
	$loggedIn=false;
}

$courseId=$_GET['course'];

database::connectToDatabase();

?>
<div id="<? echo $courseId; ?>">
	<div id="<? echo $courseId; ?>_lists">
		<div id="<? echo $courseId; ?>_lectures" class="file_list">
		<div class="select_all_checkbox"><input type="checkbox" class="select_all" id="checkL"  onclick="select_all(this.id,'<? echo $courseId;?>_lectures');"><span style="float:right;">SELECT ALL</span></div>

<?php
//		$return_lec=database::getLecObject("COURSE_ID",$courseId,"AND ".TIMESTAMP.">=now()- interval'7 days' ORDER BY ".TIMESTAMP." DESC");
		$return_lec=database::getLecObject("COURSE_ID",$courseId," ORDER BY ".TIMESTAMP." DESC");

    $l=0;
	foreach($return_lec as $result)
	{
		$l++;
$facName=mysql_fetch_array(database::executeQuery(database::getFacName($result->getFacultyId())));

?>
			<div class="link_container"><div class="reg_fac"><? echo $facName[0]; ?></div><a target="_blank" class="file_reg list_selected <? echo $courseId; ?>" href="<? echo LECDIR; ?>/<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"><? echo " ".$result->getTopic(); ?></a>
			<input type="checkbox" name="lec[]" class="chk" id="lec_<?php echo $l; ?>" value="<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"></div>
<?php
	}
	if($l==0)
	{
//		echo "No new lectures in last week.";
		echo "No new lectures.";
  }
?>
		</div>
		<div id="<? echo $courseId; ?>_tutorials" class="file_list">
		<div class="select_all_checkbox"><input type="checkbox" class="select_all" id="checkT"  onclick="select_all(this.id,'<? echo $courseId;?>_tutorials');"><span style="float:right;">SELECT ALL</span></div>

<?php

	//		$return_tut=database::getTutObject("COURSE_ID",$courseId,"AND ".TIMESTAMP.">=now()- interval'7 days' ORDER BY ".TIMESTAMP." DESC");
	$return_tut=database::getTutObject("COURSE_ID",$courseId," ORDER BY ".TIMESTAMP." DESC");
		$t=0;
	foreach($return_tut as $result)
	{	
		$t++;
$facName=mysql_fetch_array(database::executeQuery(database::getFacName($result->getFacultyId())));

?>
			<div class="link_container"><div class="reg_fac"><? echo $facName[0]; ?></div><a target="_blank" class="file_reg list_selected <? echo $courseId; ?>" href="<? echo TUTDIR; ?>/<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"><? echo " ".$result->getTopic(); ?></a>
			<input type="checkbox" name="tut[]" class="chk" id="tut_<? echo $t; ?>" value="<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"></div>
<?php
	}
	if($t==0)
	{
	//		echo "No new tutorials in last week.";
	echo "No new tutorials.";
	}

?>
		</div>
		<div id="<? echo $courseId; ?>_exam_papers" class="file_list">
		<div class="select_all_checkbox"><input type="checkbox" class="select_all" id="checkE"  onclick="select_all(this.id,'<? echo $courseId;?>_exam_papers');"><span style="float:right;">SELECT ALL</span></div>

<?php

	//		$return_exam=database::getExamPaperObject("COURSE_ID",$courseId,"AND ".TIMESTAMP.">=now()- interval'7 days' ORDER BY ".TIMESTAMP." DESC");
	$return_exam=database::getExamPaperObject("COURSE_ID",$courseId," ORDER BY ".TIMESTAMP." DESC");
		$e=0;
	foreach($return_exam as $result)
	{	
		$e++;
$facName=mysql_fetch_array(database::executeQuery(database::getFacName($result->getFacultyId())));

?>
			<div class="link_container"><div class="reg_fac"><? echo $facName[0]; ?></div><a target="_blank" class="file_reg list_selected <? echo $courseId; ?>" href="<? echo EXAMDIR; ?>/<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"><? echo " ".$result->getTopic(); ?></a>
			<input type="checkbox" name="exam[]" class="chk" id="exam_<? echo $e; ?>"value="<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"></div>
<?php
	}
	if($e==0)
	{
	//		echo "No new exam papers in last week.";
	echo "No new exam papers.";
	}

?>
		</div>
		<div id="<? echo $courseId; ?>_solutions" class="file_list">
		<div class="select_all_checkbox"><input type="checkbox" class="select_all" id="checkS"  onclick="select_all(this.id,'<? echo $courseId;?>_solutions');"><span style="float:right;">SELECT ALL</span></div>

<?php
	//		$return_soln=database::getSolnObject("COURSE_ID",$courseId,"AND ".TIMESTAMP.">=now()- interval'7 days' ORDER BY ".TIMESTAMP." DESC");
	$return_soln=database::getSolnObject("COURSE_ID",$courseId," ORDER BY ".TIMESTAMP." DESC");
		$s=0;
	foreach($return_soln as $result)
	{	
		$s++;
$facName=mysql_fetch_array(database::executeQuery(database::getFacName($result->getFacultyId())));

?>
			<div class="link_container"><div class="reg_fac"><? echo $facName[0]; ?></div><a target="_blank" class="file_reg list_selected <? echo $courseId; ?>" href="<? echo SOLNDIR; ?>/<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"><? echo " ".$result->getTopic(); ?></a>
			<input type="checkbox" name="soln[]" class="chk" id="soln_<? echo $s; ?>" value="<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"></div>
<?php
	}
	if($s==0)
	{
	//		echo "No new solutions in last week.";
	echo "No new solutions.";
	}

?>
		</div>
		<div id="<? echo $courseId; ?>_all" class="file_list">
		<div class="select_all_checkbox"><input type="checkbox" class="select_all" id="checkA"  onclick="select_all(this.id,'<? echo $courseId;?>_all');"><span style="float:right;">SELECT ALL</span></div>

<?php
	$l=0;
	echo "<div class='file_list' id='lec_all' style='width:100%; font-size:18px'>Lectures</div>";
	foreach($return_lec as $result)
	{
			$l++;
$facName=mysql_fetch_array(database::executeQuery(database::getFacName($result->getFacultyId())));

?>
			<div class="link_container"><div class="reg_fac"><? echo $facName[0]; ?></div><a target="_blank" class="file_reg list_selected <? echo $courseId; ?>" href="<? echo LECDIR; ?>/<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"><? echo " ".$result->getTopic(); ?></a>
			<input type="checkbox" name="lec[]" class="chk_all" id="lec_<?php echo $l; ?>" value="<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"></div>

<?php
	}
	if($l==0)
	{
	//		echo "<div class='file_list' id='exam_all' style='width:100%;text-align:center;'>No New Lectures in Last week</div>";
	echo "<div class='file_list' id='exam_all' style='width:100%;text-align:center;'>No New Lectures</div>";
	}
	echo "<br>";
	$t=0;
	echo "<div class='file_list' id='tut_all' style='width:100%; font-size:18px'>Tutorials</div>";
	foreach($return_tut as $result)
	{	
			$t++;
$facName=mysql_fetch_array(database::executeQuery(database::getFacName($result->getFacultyId())));

?>
			<div class="link_container"><div class="reg_fac"><? echo $facName[0]; ?></div><a target="_blank" class="file_reg list_selected <? echo $courseId; ?>" href="<? echo TUTDIR; ?>/<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"><? echo " ".$result->getTopic(); ?></a>
			<input type="checkbox" name="tut[]" class="chk_all" id="tut_<? echo $t; ?>" value="<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"></div>

<?php
	}	
	if($t==0)
	{
	//		echo "<div class='file_list' id='exam_all' style='width:100%;text-align:center;'>No New Tutorials in Last week</div>";
	echo "<div class='file_list' id='exam_all' style='width:100%;text-align:center;'>No New Tutorials</div>";
	}
	echo "<br>";
	$e=0;
	echo "<div class='file_list' id='exam_all' style='width:100%; font-size:18px;'>Exam Papers</div>";
	foreach($return_exam as $result)
	{	
			$e++;
$facName=mysql_fetch_array(database::executeQuery(database::getFacName($result->getFacultyId())));

?>
			<div class="link_container"><div class="reg_fac"><? echo $facName[0]; ?></div><a target="_blank" class="file_reg list_selected <? echo $courseId; ?>" href="<? echo EXAMDIR; ?>/<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"><? echo " ".$result->getTopic(); ?></a>
			<input type="checkbox" name="exam[]" class="chk_all" id="exam_<? echo $e; ?>"value="<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"></div>
<?php
	}	
	if($e==0)
	{
	//		echo "<div class='file_list' id='exam_all' style='width:100%;text-align:center;'>No New Exam Papers in Last week</div>";
	echo "<div class='file_list' id='exam_all' style='width:100%;text-align:center;'>No New Exam Papers</div>";
	}
	echo "<br>";
	$s=0;
	echo "<div class='file_list' id='soln_all' style='width:100%; font-size:18px'>Solutions</div>";
	foreach($return_soln as $result)
	{	
			$s++;
$facName=mysql_fetch_array(database::executeQuery(database::getFacName($result->getFacultyId())));

?>
			<div class="link_container"><div class="reg_fac"><? echo $facName[0]; ?></div><a target="_blank" class="file_reg list_selected <? echo $courseId; ?>" href="<? echo SOLNDIR; ?>/<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"><? echo " ".$result->getTopic(); ?></a>
			<input type="checkbox" name="soln[]" class="chk_all" id="soln_<? echo $s; ?>" value="<? echo $result->getFacultyId(); ?>/<? echo $result->getFile(); ?>"></div>

<?php
	}
	if($s==0)
	{
	//		echo "<div class='file_list' id='exam_all' style='width:100%; text-align:center;'>No New Solutions in Last week</div>";
	echo "<div class='file_list' id='exam_all' style='width:100%; text-align:center;'>No New Solutions</div>";
	}

?>
		</div>

	</div>
</div>
<?php

database::closeDatabase();
?>
