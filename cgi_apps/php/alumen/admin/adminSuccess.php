<?php
session_start();
if(!isset($_SESSION["admin_user"]))
	header("Location: adminLogout.php");

include('../connection.php');
include_once("adminloggedin.html");

/**************************functions**************************/
require('../common.php');
/***********************************************************/
/* The second arguement "username" is a mode where only session authentication is done. the other mode is "both" where both username and passwd are to be passed*/
if(isset($_SESSION["admin_user"]))
{

		
		/* There is a separate displayAction.js for admin functions. In "js" directory inside admin directory*/
	
		echo "<script language='javascript'>";
		echo "document.location+='#ShowUsers';";
		echo "updateInfo('ShowUsers',1)";
		echo "</script>";
		 


}	

pg_close($dbcon);
?>
