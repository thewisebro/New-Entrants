<?php

//session_start();

include_once("../common/functions.php");
include("../../session/django_session.php");
$session = new Session();

database::connectToDatabase();

$depCode=$_GET['profList'];
$dept=$_GET['depCode'];
$dep_code=array();
$dep_code=explode(",",$depCode);
echo "<div id='$dept' class=\"department_prof_div\" >";
  foreach($dep_code as $fac_id)
	{
    $facUserId=mysql_fetch_array(database::executeQuery(database::getFacUserId($fac_id)));
		$result=database::executeQuery(database::getFacName($facUserId[0]));
		if($result)
		{
			$facName=mysql_fetch_array($result);
?>	
			<div id="<? echo $fac_id; ?>"><a href="javascript:prof_goto('#browse_by_department_course_selection','<? echo $fac_id; ?>','<? echo $facName[0]; ?>');" class="profs_dept prof_active"><? echo $facName[0]; ?></a></div><br>
<?
		}
	}
echo "</div>";
database::closeDatabase();

?>			
