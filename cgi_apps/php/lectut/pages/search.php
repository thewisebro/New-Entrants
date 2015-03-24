<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<?php
//session_start();

include_once("../common/functions.php");
include("../../session/django_session.php");
$session = new Session();

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

?>

<html>
	<head>
		<title>Lectures and Tutorials</title>
<?php		include_once("../common/styles.php"); ?>
	</head>
	<body onload="javascript:s();">
		<div class="search_container" id="my_courses_goto">
			<div id="mcl_container"> 
				<div id="mcl">
				</div> 
				<a href="javascript:func1('#main_goto');"><div class="link_space"></div></a>
				<a href="javascript:func1('#browse_by_department_goto');"><div class="link_space"></div> </a>
			</div>
		<div id="searchr"></div>
		<div id="search_play_area" >
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
			<div id="search_page_container">
				<div id="search_topbar">
					<div id="search_logout_button" >
<?php
	if($loggedIn)
	{
			echo "<a href=\"/nucleus/logout\">LOGOUT</a>";
	}
	else
	{
    echo "<a href=\"index.php\">LOGIN</a>";
	}	
?>		
					</div>
					<div id="search_title">SEARCH RESULTS</div>
					<div id="welcome_text">
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

database::connectToDatabase();

if(isset($studId))
{
	$reg_courses=database::executeQuery(database::studQuery($studId));
}
$time1=microtime(true);
$results_lec = search_perform($search,"lec");
$results_tut = search_perform($search,"tut");
$results_exam = search_perform($search,"exam");
$results_soln = search_perform($search,"soln");
$time2=microtime(true);
$time=$time2-$time1;
$time=round($time,3);

echo "$search ($time seconds)";
}
?>
					</div>
				</div>
				<div id="search_selection">
					<a href="javascript:func2_search('#search_lectures','#scroll_search_target','#my_courses_lectures_link');"  id="my_courses_lectures_link" class="search_selection_link search_inactive_link search_link">LECTURES</a>
					<a href="javascript:func2_search('#search_tutorials','#scroll_search_target','#my_courses_tutorials_link');"  id="my_courses_tutorials_link" class="search_selection_link search_inactive_link search_link">TUTORIALS</a>
					<a href="javascript:func2_search('#search_exam_papers','#scroll_search_target','#my_courses_exam_papers_link');"  id="my_courses_exam_papers_link" class="search_selection_link search_inactive_link search_link">EXAM PAPERS</a>
					<a href="javascript:func2_search('#search_solutions','#scroll_search_target','#my_courses_solutions_link');"  id="my_courses_solutions_link" class="search_selection_link search_inactive_link search_link">SOLUTIONS</a>
				</div>
		<form name="download" action="download.php" method="post" onsubmit="return validate_form()">
					<div id="search_files">



					<div class="scrollbarer">
					
					<div class="scrollbar"><div class="track"><div class="thumb"><div class="end"></div></div></div></div>
<!-- this set and not overview as this is the relatively outermost container div  -->
				<div class="viewport" id="scroll_search_target">
			 <div class="overview" >

						<div id="subjects" class="search_tabs">
<div id="search_lectures" class="file_list" style="width:25%;">
<div class="select_all_checkbox"><input type="checkbox" class="select_all" id="checkL" style="margin-right:60px;"  onclick="select_all(this.id,'search_lectures');"><span style="float:right;">SELECT ALL</span></div>

<?php
$i=count($results_lec);
$count=0;
foreach($results_lec as $result)
{       
	if($result[0]->getPermission()==0 || in_array($result[0]->getCourseId(),$reg_courses) || $facId==$result[0]->getFacultyId())
	{
		$count++;
		$facName=mysql_fetch_array(database::executeQuery(database::getFacName($result[0]->getFacultyId())));

?>	<div class="record"><span class="serial_no"><? echo $count; ?></span><span class="prof_name"><? echo $facName[0]; ?></span><span class="course_id"><? echo $result[0]->getCourseId(); ?></span><span><a class="file_link list_selected lecture" target="_blank" href="<? echo LECDIR."/".$result[0]->getFacultyId()."/".$result[0]->getFile(); ?>"><? echo $result[0]->getTopic(); ?></a></span><input class="chk" type="checkbox" name="lec[]" value="<? echo $result[0]->getFacultyId()."/".$result[0]->getFile(); ?>">
</div>
<?php   
	}
}       
if($count==0)
{
echo "No lectures found.";
}       
?>
</div>

<div id="search_tutorials" class="file_list" style="width:25%;">
<div class="select_all_checkbox"><input type="checkbox" class="select_all" id="checkT" style="margin-right:60px;"  onclick="select_all(this.id,'search_tutorials');"><span style="float:right;">SELECT ALL</span></div>

<?php
$i=count($results_tut);
$count=0;
foreach($results_tut as $result)
{       
	if($result[0]->getPermission()==0 || in_array($result[0]->getCourseId(),$reg_courses) || $facId==$result[0]->getFacultyId())
	{
		$count++;
		$facName=mysql_fetch_array(database::executeQuery(database::getFacName($result[0]->getFacultyId())));

?>
		<div class="record"><span class="serial_no"><? echo $count; ?></span><span class="prof_name"><? echo $facName[0]; ?></span><span class="course_id"><? echo $result[0]->getCourseId(); ?></span><span><a class="file_link list_selected tutorial" target="_blank" href="<? echo TUTDIR."/".$result[0]->getFacultyId()."/".$result[0]->getFile(); ?>"><? echo $result[0]->getTopic(); ?></a></span><span><input class="chk" type="checkbox" name="tut[]" value="<? echo $result[0]->getFacultyId()."/".$result[0]->getFile(); ?>">
</span></div>
<?php   
	}       
}       
if($count==0)
{
echo "No tutorials found.";
}       
?>
</div>

<div id="search_exam_papers" class="file_list" style="width:25%;">
<div class="select_all_checkbox"><input type="checkbox" class="select_all" id="checkE" style="margin-right:60px;"  onclick="select_all(this.id,'search_exam_papers');"><span style="float:right;">SELECT ALL</span></div>

<?php
$i=count($results_exam);
$count=0;
foreach($results_exam as $result)
{       
	if($result[0]->getPermission()==0 || in_array($result[0]->getCourseId(),$reg_courses) || $facId==$result[0]->getFacultyId())
	{
		$count++;
		$facName=mysql_fetch_array(database::executeQuery(database::getFacName($result[0]->getFacultyId())));

?>
		<div class="record"><span class="serial_no"><? echo $count; ?></span><span class="prof_name"><? echo $facName[0]; ?></span><span class="course_id"><? echo $result[0]->getCourseId(); ?></span><span ><a class="file_link list_selected exam_paper" target="_blank" href="<? echo EXAMDIR."/".$result[0]->getFacultyId()."/".$result[0]->getFile(); ?>"><? echo $result[0]->getTopic(); ?></a></span><span><input class="chk" type="checkbox" name="exam[]" value="<? echo $result[0]->getFacultyId()."/".$result[0]->getFile(); ?>">
</span></div>
<?php   
	}       
}       
if($count==0)
{
echo "No exam papers found.";
}       
?>
</div>

<div id="search_solutions" class="file_list" style="width:25%;">
<div class="select_all_checkbox"><input type="checkbox" class="select_all" id="checkS" style="margin-right:60px;" onclick="select_all(this.id,'search_solutions');"><span style="float:right;">SELECT ALL</span></div>

<?php
$i=count($results_soln);
$count=0;
foreach($results_soln as $result)
{       
	if($result[0]->getPermission()==0 || in_array($result[0]->getCourseId(),$reg_courses) || $facId==$result[0]->getFacultyId())
	{
		$count++;
		$facName=mysql_fetch_array(database::executeQuery(database::getFacName($result[0]->getFacultyId())));

?>
		<div class="record"><span class="serial_no"><? echo $count; ?></span><span class="prof_name"><? echo $facName[0]; ?></span><span class="course_id"><? echo $result[0]->getCourseId(); ?></span><span><a class="file_link list_selected solution" target="_blank" href="<? echo SOLNDIR."/".$result[0]->getFacultyId()."/".$result[0]->getFile(); ?>"><? echo $result[0]->getTopic(); ?></a></span><span><input class="chk" type="checkbox" name="soln[]" value="<? echo $result[0]->getFacultyId()."/".$result[0]->getFile(); ?>">
</span></div>
<?php   
	}       
}       
if($count==0)
{
echo "No solutions found.";
}      
?>
</div>
</div>
</div>
</div>

	
								</div>
							</div>
				<div style="margin-top:20px;">
				<input type="submit" value="Download selected" class="download_button" id="d_button_mc">
				</form>
				<a id="search_box_link_" href="javascript:s();search_focus();">
					<div id = "search_link_main">Search</div>
				</a>
				</div>
			</div>
		</div>
	</div>
	<div class="search search_unfocused">

		<div href="#" class="close-meerkat">X</div>

		<div id="search_box">	
			<form name="search" action="search.php" method="get">
				<input name="search" type="text" id="search_input" onfocus="javascript:search_focus();" onblur="javascript:search_unfocus();">
				<input type="submit" id="search_submit" value="Search">
			</form>
		</div>
	</div>
  <script type="text/javascript" src="/static/js/piwik.js"></script>  
</body>
<!--[if !(IE 6)]><!-->
	<script>s()</script>
<!--<![endif]-->
<!--[if IE 6]>
	
	<script>s();load();</script>
<![endif]-->

</html>
<?php

database::closeDatabase();

?>
