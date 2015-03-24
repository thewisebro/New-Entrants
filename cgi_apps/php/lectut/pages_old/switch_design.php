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

if($loggedIn && $_SESSION['group']=='s')
{
	header("Location: ../pages/final_student.php");
}

$facUsername=$_SESSION['lectut_username'];

database::connectToDatabase();

$result=database::executeQuery(database::deleteDesignChoice($facUsername));

$result=database::executeQuery(database::insertDesignChoice($facUsername,0));

header("Location: ../pages/final_prof.php");

database::closeDatabase();

?>
