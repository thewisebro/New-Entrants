<?php
session_start();
error_reporting(E_ALL);
ini_set('display_errors',1);

if(!isset($_SESSION["username"])) 
{
	header("Location: logout.php");
	die();
}

include("../connection.php");
include_once("common.php");

$alumni = $_SESSION["username"];

if(MentorshipAscessOfAlumni($alumni,$dbcon))
{

$mails = retrieveFromDb($dbcon,"conversation","sender,receiver,subject,time,mail,serial","receiver='rishabh' order by time desc");

if($mails)
{

	echo "<fieldset><legend>Your messages</legend>";
	$limit = count($mails);
	echo "<br /><table border ='1' style ='empty-cells:show; text-align:left' cellspacing='0' cellpadding='5'>";
	echo "<th>S. NO.</th><th>FROM</th><th>SUBJECT</th><th>TIME</th>";
	
	for($i=0;$i<$limit;$i++)
	{
		echo "<tr><td>".($i+1)."</td>";
		echo "<td><a href='student/readMail.php?mail=".$mails[$i]['mail']."'>".$mails[$i]['sender']."</a></td>";
		echo "<td><a href='#'>".$mails[$i]['subject']."</a></td>";
		echo "<td>".$mails[$i]['time']."</td>";
	
		echo "</tr>";
	}
		
	echo "</table></fieldset><br />";
}
}


?>
<html>
<body>
<fieldset>
<legend>Conversation</legend>
</fieldset>
</body>
</html>
