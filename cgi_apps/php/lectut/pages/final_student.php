<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<?php

//session_start();
include_once("../common/functions.php");
include("../../session/django_session.php");
$session = new Session();

$loggedIn=false;
//if(isLogin($_SESSION['username'],$_SESSION['sessionid']))
//{
if($session->isloggedin())
{
  if($_SESSION['group']=='s')	
		$studId=$_SESSION['lectut_userid'];
  else if($_SESSION['group']=='f')
		$facId=$_SESSION['lectut_userid'];
	$loggedIn=true;
}
else
{
	$loggedIn=false;
}
?>

<html>
	<head>
		<title>Lectures and Tutorials</title>
<?php		include_once("../common/styles.php"); ?>
	</head>
	<body>
	<div id="container">
	<div id="spacer">
<?php	
	include_once("../pages/dept_list.php"); 
if($loggedIn && $_SESSION['group']=='s')
{
?>
		<div class="ss"id="main_goto">
			<div id="mainl"></div>
			<div id="mainr"></div>
			<div id="main" class="main">
				<div id="main_topbar">
<?php
	
	
	
	if(!$loggedIn)
	{
		echo "<a class=\"logout_button\" href=\"index.php\">LOGIN</a>";
	}
	else
	{
		echo "<a class=\"logout_button\" href=\"/nucleus/logout\">LOGOUT</a>";
	}
	echo '<a class="logout_button" href="/" style="float:left; margin-right:0px; margin-left:50px;">CHANNEL I</a>';
?>	
					
					<div id="main_title">LECTURES AND TUTORIALS</div>
				</div> 
				<div id="main_intro">
				<? include_once("welcome.php");  ?>
				</div>
				<div id="navigator">
				What would you like to do? <br>
				<!--[if !(IE 6)]><!-->				
				<a id="browse_by_department_link" href="javascript:func1('#browse_by_department_goto');">
				<!--<![endif]-->
				<!--[if IE 6]>
				<a id="browse_by_department_link" href="javascript:ie_func1('#browse_by_department_goto');">
				<![endif]-->
				Browse courses by department</a> <br/>
<?php
if($loggedIn && $_SESSION['group']=='s')
{
echo "
<!--[if !(IE 6)]><!-->
<a id=\"my_courses_link\" href=\"javascript:func1('#my_courses_goto');\">
<!--<![endif]-->
<!--[if IE 6]>
<a id=\"my_courses_link\" href=\"javascript:ie_func1('#my_courses_goto');\">
<![endif]-->
View registered courses </a><br>";

} 
else
{
	echo "<a id=\"my_courses_link\" href=\"index.php\">Login</a><br/>";
}
?>
				<a id="search_box_link_main" href="javascript:s();">Search for lectures/tutorials</a>
				</div>
			</div>
		</div>
<?php
}

if($loggedIn && $_SESSION['group']=='s')
{
	include_once("../pages/student.php"); 
}
?>
	</div>
</div>
<div class="search search_unfocused">
	<div href="#" class="close-meerkat">X</div>
	<div id="search_box">
		<form name="search" action="search.php" method="get">
		<input name="search" type="text" id="search_input" onfocus="javascript:search_focus();" onblur="javascript:search_unfocus();">
		<input type="submit" id="search_submit" value="Search">
		</form>
	</div>
</div>

<? include_once("facebox.php"); ?>

<script type="text/javascript" src="/static/js/piwik.js"></script>
	</body>
<!--[if !(IE 6)]><!-->
	<script></script>
<!--<![endif]-->
<!--[if IE 6]>
	
	<script>load();</script>
	<script>ie_func1('#browse_by_department_goto');s();</script>
<![endif]-->

</html>
