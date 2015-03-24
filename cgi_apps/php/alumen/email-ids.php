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
//echo $new_email_id.$username;

$infoArray=retrieveFromDb($dbcon,"emails","email_ids,counter","username='$username'");
$info=$infoArray[0];
if($infoArray==null)
{
	$query="insert into emails values('$username','$new_email_id',9)";
}
else
{	
	if($info['counter']>0)
		{

			//		$old_email_idArray=retrieveFromDb($dbcon,"emails","email_ids","username='$username'");
			$x=",";
			$email_ids=$new_email_id.$x.$info['email_ids'];
			$counter=$info['counter']-1;
			//		echo $email_ids;
			$query="update emails set email_ids='$email_ids', counter=$counter  where username='$username'";

		}
		else
		{
			echo "Your 10 entries for the day is over. Please fill in the rest of email-ids tommorrow";
		}
}

$result=pg_query($dbcon,$query);

?>

