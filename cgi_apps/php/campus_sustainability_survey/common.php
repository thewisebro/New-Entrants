<?php
	session_start();
	if(!isset($_SESSION['email'])){
		session_destroy();
		header('location:index.php');
		exit();
	}
	$con = mysql_connect("192.168.121.9","survey","surv3y!") or die("Connection could not be setup <br/>"."Error in connection. Please try again."); 
	$db = mysql_select_db("campus_survey", $con) or die("Error in connection. Please try again.");
?>
