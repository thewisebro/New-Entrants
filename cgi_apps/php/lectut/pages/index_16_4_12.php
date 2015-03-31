<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<?php
//session_start();
include_once("../common/functions.php");
include("../../session/django_session.php");

$session = new Session();

?>
<html>
	<head>
		<title>Lectures and Tutorials</title>
		<?php		include_once("../common/styles.php"); ?>
	</head>
	<!--[if !IE]><!-->
        <!--[endif]-->
	<!--[if !(IE 6)]><!-->
	<body>
	<!--[endif]-->
	<!--[if IE 6]>
	<script>void(0);</script>
        <![endif]-->
	<!--[if IE 6]>
        <script>void(0);</script>
	<body>
	<![endif]-->
 <!--	
<!--[if gte IE 7]>
	<body onLoad="s(); search_focus();">
	<![endif]
-->

	

	

<div id="mainl"></div>
<div id="mainr"></div>

<div id="main" class="main">

	<div id="main_topbar">
		<a class="logout_button" href="final_student.php">
		BROWSE ALL
		</a>
		
		<a class="logout_button" href="#" onclick="s();">
		SEARCH
		</a>

		<a class="logout_button" href="/" style="float:left; margin-right:0px; margin-left:50px;">
		CHANNEL I
		</a>
<?php

//if(isLogin($_SESSION['username'],$_SESSION['sessionid']))
//{
if($session->isloggedin())
{
	if($_SESSION['group']=='s')	
		header("Location: final_student.php");
  else if($_SESSION['group']=='f')
		header("Location: final_prof.php");
}?>

		<div id="main_title">
		LECTURES AND TUTORIALS
		</div>
	</div> 

	<div id="main_intro">
		
							Welcome to the new lectures and tutorials webpage. Here you may find various lectures,tutorials, exams papers and solutions as submitted by the respective faculty. Please login to proceed.
		
	</div>

	<!--<form action="search.php" method="get">   
		<input type="text" name="search">
		<input type="Submit" value="Search">
	</form>-->
	
	<form id="login_form" method="post" action="auth.php" name="login_form" onsubmit="return check_login();">
<?php
	$temp=$_GET['temp'];
	echo "<div id='warning' style='font-size:14px; color:#B00; text-align:right;float: left;width: 250px;'>";
	if(isset($temp))
	{
		if ($temp=='l')
			echo "Wrong username/password !";
		else if ($temp=='s')
			echo "Session expired. Please login again !";
	}
	echo "</div>";
?>	
	<input type="text" name="username" id="username" value="Username" class="form" onfocus="user_input_focus('#search_input');" onblur="user_input_unfocus('#search_input');"/><br/>
	<input type="text" name="fakepassword" id="password_show" value="Password" class="form" onfocus="fake_focus();"/>
	<input type="password" name="password" id="password" value="" class="form" onblur="real_blur();"/><br/>	
	<input type="submit" name="Submit" value="Login" id="login_button" style="cursor:pointer;">
	</form>
	
</div>
<div class="search search_unfocused">
	<div href="#" class="close-meerkat">X</div>
	<div id="search_box">
		<form name="search" action="search.php" method="get">
		<input name="search" type="text" id="search_input" onfocus="javascript:search_focus('');" onblur="javascript:search_unfocus();">
		<input type="submit" id="search_submit" value="Search">
		</form>
	</div>
</div>
	
	</body>
<!--[if !(IE 6)]><!-->
	<script>s();search_focus();</script>
<!--<![endif]-->
<!--[if IE 6]>
	
	<script>load();s();search_focus();</script>
<![endif]-->

<!-- Piwik --> 
<script type="text/javascript">
var pkBaseURL = (("https:" == document.location.protocol) ? "https://192.168.121.144/php/piwik/" : "http://192.168.121.144/php/piwik/");
document.write(unescape("%3Cscript src='" + pkBaseURL + "piwik.js' type='text/javascript'%3E%3C/script%3E"));
</script><script type="text/javascript">
try {
  var piwikTracker = Piwik.getTracker(pkBaseURL + "piwik.php", 5);
  piwikTracker.trackPageView();
  piwikTracker.enableLinkTracking();
} catch( err ) {}
</script><noscript><p><img src="http://192.168.121.144/php/piwik/piwik.php?idsite=5" style="border:0" alt="" /></p></noscript>
<!-- End Piwik Tracking Code -->

</html>
