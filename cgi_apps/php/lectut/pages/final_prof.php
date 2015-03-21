<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
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

if($loggedIn && $_SESSION['group']=='s')
{
	header("Location: final_student.php");
}

$facUsername=$_SESSION['lectut_username'];

?>
<html>
	<head>
		<title>Lectures and Tutorials</title>
<?php		include_once("../common/styles.php"); ?>
	</head>
	<body>
<?php
if($loggedIn && $_SESSION['group']=='f')
{
     database::connectToDatabase();
     $result=database::executeQuery(database::getDesignChoice($facUsername));
     if(mysql_fetch_row($result)==NULL)
     {
         database::executeQuery("intranet",database::insertDesignChoice($facUsername,0));
     echo "<div id=\"doyou\" style=\"position: fixed; height: 150px; width: 400px; top: 50%; left: 50%; _position:absolute; _top:expression(eval(document.body.scrollTop)+200); _left:expression(eval(document.body.scrollLeft)+200px); margin-left: -200px; background-color: white; font-family: 'bebas neue'; font-size: 25px; z-index: 1000; text-align: center; border-top-width: 4px; border-right-width: 4px; border-bottom-width: 4px; border-left-width: 4px; border-top-style: solid; border-right-style: solid; border-bottom-style: solid; border-left-style: solid; border-top-color: rgb(191, 207, 4); border-right-color: rgb(191, 207, 4); border-bottom-color: rgb(191, 207, 4); border-left-color: rgb(191, 207, 4); border-image: initial; display : inline; \"><div style=\"height: 30px;width:100%;text-align:right;\"><a href=\"javascript:void(0)\" onclick=\"hide_doyou();\" style=\"
             color: #eb6864;
         padding-right: 5px;
         \">x</a></div>Don't like the new look? <br><a href=\"switch_design.php\" style=\"color: #eb6864;\">click here to Switch back</a></div>";
 
     }
     database::closeDatabase();
 }
?>
<?php
/*if($loggedIn!=0 && $_SESSION['group']=='f')
{
     database::connectToDatabase("intranet");
     $result=database::executeQuery("intranet",database::getDesignChoice($facId));
     if(pg_fetch_row($result)==NULL)
     {
         database::executeQuery("intranet",database::insertDesignChoice($facId,'false'));
     	echo "<div id=\"doyou\" style=\"position: fixed; height: 150px; width: 400px; top: 50%; left: 50%; margin-left: -200px; background-color: white; font-family: 'bebas neue'; font-size: 25px; z-index: 1000; text-align: center; border-top-width: 4px; border-right-width: 4px; border-bottom-width: 4px; border-left-width: 4px; border-top-style: solid; border-right-style: solid; border-bottom-style: solid; border-left-style: solid; border-top-color: rgb(191, 207, 4); border-right-color: rgb(191, 207, 4); border-bottom-color: rgb(191, 207, 4); border-left-color: rgb(191, 207, 4); border-image: initial; display: inline; \"><div style=\"height: 30px;width:100%;text-align:right;\"><a onclick = \"function change(){document.getElementById('doyou').style.display = 'none';}\" href=\"#\"style=\"
    color: #eb6864;
    padding-right: 5px;
\">x</a></div>Don't like the new look? <br><a href=\"switch_design.php\" style=\"color: #eb6864;\">click here to Switch back</a></div>";
     }
     database::closeDatabase("intranet");
}*/
?>

<div id="container">
	<div id="spacer">
<?php
if($loggedIn && $_SESSION['group']=='f')
{
	include_once("../pages/faculty.php"); 
}
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
							Welcome to the new lectures and tutorials webpage. Here you may find various lectures,tutorials, exams papers and solutions as submitted by the respective faculty. Please select one of the links given below to proceed.
<?php
if($loggedIn && $_SESSION['group']=='f')
{
     echo "<br/><br/><a style=\"color:#BFCF04\" href=\"switch_design.php\">Click here to go to old LecTut</a>";
}
?>
				</div>
				<div id="navigator">
				What would you like to do? <br>
<?php
if($loggedIn)
{
	echo " 
<!--[if !(IE 6)]><!-->
<a id=\"browse_by_department_link\" href=\"javascript:func1('#browse_by_department_goto');\">
<!--<![endif]-->
<!--[if IE 6]>
<a id=\"browse_by_department_link\" href=\"javascript:ie_func1('#browse_by_department_goto')\">
<![endif]-->
Upload</a><br/>
<!--[if !(IE 6)]><!-->
<a id=\"my_courses_link\" href=\"javascript:func1('#my_courses_goto');\">
<!--<![endif]-->
<!--[if IE 6]>
<a id=\"my_courses_link\" href=\"javascript:ie_func1('#my_courses_goto');\">
<![endif]-->
Manage Files</a><br/><a id=\"browse_by_department_link_2\" href=\"final_student.php\" style=\"font-size:20px;width:410px; \">Browse By Department</a><br>";
}
else
{
	echo "<a id=\"my_courses_link\" href=\"index.php\">Login</a><br>";
}
?>
				<a id="search_box_link_main" href="javascript:s();">Search for lectures/tutorials</a>
				</div>
			</div>
		</div>	
<?php
if($loggedIn && $_SESSION['group']=='f')
{
	include_once("../pages/managefiles.php"); 
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

<? include_once("facebox.php");?>
<script type="text/javascript" src="/static/js/piwik.js"></script>  
  </body>
<!--[if !(IE 6)]><!-->
	<script></script>
<!--<![endif]-->
<!--[if IE 6]>
	
	<script>load();ie_func1('#main_goto');</script>
<![endif]-->


</html>
