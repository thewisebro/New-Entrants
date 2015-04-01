<?php
//session_start();

include_once("../common/functions.php");
include("../../session/django_session.php");
$session = New Session();

if($_SESSION['group']=='f')
	$facId=$_SESSION['lectut_userid'];

database::connectToDatabase();

$facUsername=$_SESSION['lectut_username'];

$type=$_GET["type"];
$subcode=secureCode($_GET["subcode"]);

switch($type)
{
	case 'T':
		$return_tut=database::getTutObject("FACULTY_ID",$facUsername,null);
if(!empty($return_tut))
{
	$i=1;
	foreach($return_tut as $result)
	{
	if($subcode==null ||$subcode==$result->getCourseId()){
?>
	<div class="file_list" style="width:600px;">
		<div style="float:left; width:20px;">
		<? echo $i++; ?>
		</div>
		<div style="float:left; width:100px;">
		<? echo $result->getCourseId(); ?>
		</div>
		<div style="float:left; width:400px;">
		<? echo $result->getTopic(); ?>
		</div>
		<div style="float:left; width:20px;">
			<input type="radio" name="link_tut" value="<? echo $result->getId(); ?>">
		</div>
	</div>
	<br>
<?
	}
	}
}	
		break;

	case 'E':
		$return_exam=database::getExamPaperObject("FACULTY_ID",$facUsername,null);
if(!empty($return_exam))
{
	$i=1;
	foreach($return_exam as $result)
	{
	if($subcode==null ||$subcode==$result->getCourseId()){
?>
	<div class="file_list" style="width:600px;">
		<div style="float:left; width:20px;">
		<? echo $i++; ?>
		</>
		<div style="float:left; width:100px;">
		<? echo $result->getCourseId(); ?>
		</div>
		<div style="float:left; width:400px;">
		<? echo $result->getTopic(); ?>
		</div>
		<div style="float:left; width:20px;">
			<input type="radio" name="link_exam" value="<? echo $result->getId(); ?>">
		</div>
	</div>
	<br>
<?
	}
	}
}
	 	break;

	default:break;
}

database::closeDatabase();

?>
