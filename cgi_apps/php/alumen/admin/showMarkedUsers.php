<?php
session_start();
include_once('../connection.php');
if(!isset($_SESSION["admin_user"]))
{
	header("location: adminLogout.php");


}
$username=$_SESSION["admin_user"];

/**************************************Functions**********************************/
require('../common.php');

$fields="username,enrollment_no,fullname,department,degree,passing_year";

$where_condition="status='M'";
/*We get an array of rows...basically a 2D array*/
$filledInfo=retrieveFromDb($dbcon,"basic_data",$fields,$where_condition);
/*********************************************************************************/
?>




<input type="hidden" name="username" value="<?echo $username;?>">

<span class="header">Welcome Administrator!</span><br/>
You are now logged in. You can now <b>Accept</b> or <b>Reject</b> users based on their identity as an IITR Alumni. <br/>


<?

	echo "<br/><span class='header' id='active_num'>".sizeof($filledInfo)." </span> users have been marked as <b>Possibly Invalid</b>.";


	for($i=0;$i<sizeof($filledInfo);$i++)
	{
		$user=$filledInfo[$i]["username"];
		echo "<fieldset id='$user'>";
		echo "<legend></legend>";
		$even=FALSE;
		foreach($filledInfo[$i] as $key=>$value)
		{
			if($even)
				echo "<b>".strtoupper($key)."</b>:$value<br/>";
			$even=!($even);
		}

		/***************************************Loop will continue****************************/
?>
<br/>
<input id="bt_stylish" type="button" onclick="adminAction('<?echo $user;?>','approve')" value="Approve">&nbsp;&nbsp;|&nbsp;&nbsp;<input id="bt_stylish" type="button" onclick="adminAction('<?echo $user;?>','invalid')" value="Reject">&nbsp;&nbsp;


<?
/************************loop Continues**************************************/
	echo "</fieldset>";
	}

?>





