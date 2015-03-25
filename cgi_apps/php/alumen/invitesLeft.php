<?php
error_reporting(E_ALL);
?>
<?
session_start();
include_once('connection.php');
require('common.php');

if($_SESSION["username"]==null)
{
	echo "logout.php";
}
else
{
	$username=$_SESSION["username"];
}
$new_email_id=$_GET["txtEmail"];

$infoArray=retrieveFromDb($dbcon,"emails","email_ids,counter","username='$username'");
$info=$infoArray[0];
if($infoArray==null)
{
	echo "You can enter 10 more email-ids.";
}
else
{	
	echo "You can enter ".$info['counter']." more email-ids.";
}
	?>
