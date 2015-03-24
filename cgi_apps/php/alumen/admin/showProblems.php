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

$fields="contact,problem";

$where_condition="1=1";
/*We get an array of rows...basically a 2D array*/
$filledInfo=retrieveFromDb($dbcon,"problem_data",$fields,$where_condition);
/*********************************************************************************/
?>




<input type="hidden" name="username" value="<?echo $username;?>">

<span class="header">Welcome Administrator!</span><br/>


<?



	for($i=0;$i<sizeof($filledInfo);$i++)
	{
		echo "<fieldset >";
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


<?
/************************loop Continues**************************************/
	echo "</fieldset>";
	}

?>





