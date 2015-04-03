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

if($loggedIn)
{
  echo "<a href=\"/nucleus/logout\">Logout</a><br>";
	echo "<a href=\"dept_list.php\">Browse All</a><br>";

?>
	<script src="../common/jscriptfunc.js"></script>
	<script type="text/javascript" src="../styles/jquery.js"></script>
	<script type="text/javascript" src="../styles/jquery.scrollTo-1.4.2-min.js"></script>
	<script type="text/javascript" src="../styles/jquery.meerkat.1.3.min.js"></script>
	<script type="text/javascript" src="../styles/action.js"></script>
	<script type="text/javascript" src="../styles/search.js"></script>
	<script type="text/javascript" src="../styles/jquery.tinyscrollbar.min.js"></script>

	<form action="search.php" method="get">   
	<input type="text" name="search">
	<input type="Submit" value="Search">
	</form>
<?
}
else
{
	header("Location: index.php?temp=p");
}


?>

