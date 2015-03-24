
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<link rel="stylesheet" href="css/styles.css" />
	<link type="text/css" rel="stylesheet" href="css/formCss.css" />

<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Alumni Mentorship Programme :: Indian Institute Of Technology, Roorkee</title>
<script language="javascript" src="js/mandatory_fields.js"></script>
<script language="javascript" src="js/displayAction.js"></script>

<!--  facebox portion begins  
<script src="js/jquery.js" type="text/javascript"></script>
<script src="facebox/facebox.js" type="text/javascript"></script>
<link href="facebox/facebox.css" media="screen" rel="stylesheet" type="text/css"/>
<script src="js/jquery_function.js" type="text/javascript"></script>
   facebox portion ends       -->                       

</head>
<body onload="initializePage()" onBeforeUnload="if(document.getElementById('notSubmit')){if(document.getElementById('notSubmit').value==1)return '';}">
	
<div id="container">
	<div id="top">
		<div id="main_banner"><img src="images/alumni_mentorship.gif" alt="Alumni Mentorship" /></div>
		<div id="iitr_logo"><img src="images/iitr_logo.jpg" alt="IIT Roorkee"></div>
		<div id="main_links"></div>
	</div>
	<div class="divider">&nbsp;</div>
	<div class="divider">&nbsp;</div>
	<div id="bottom">
		<div id="middle_left">
	<input type="hidden" id="intro_text">
			<div id="middle_left_top">
			
				Submitting your information...<br/>
				If the form submission takes too long, click <a href="javascript:history.go(-1);">here</a> to go back and submit again.   			

			</div>
		</div>
		
		<div id="middle_right">
		
		<div id="side_box">
			<div id="image_pane">
			<div id="snapshot">Snapshots@IITR</div>
				
			<img name="SlideShow" src="images/1.jpg" alt="Snapshots@IIT Roorkee">
			
			</div>


			<span class="header"><a href="#Introduction" onclick="updateInfo('Introduction',1)">Introduction</a></span><br /><br />
			<span class="header"> <a href="#Message" onclick="updateInfo('Message',1)">Message from the Dean</a></span><br /><br />
			<span class="header"> <a href="#Guidelines" onclick="updateInfo('Guidelines',1)">Guidelines</a></span><br /><br />
			<div id="separator"></div>
			<?
			if($_SESSION['studentdata']||!(isset($_SESSION['studentdata'])))
			{	
				echo '<span class="header"> <a href="#StudentProfile" onclick="updateInfo(\'StudentProfile\',1)">Profile</a></span><br /><br />';
				echo '<div id="separator"></div>';
				echo '<span class="header"> <a href="#Mentorship" onclick="updateInfo(\'Mentorship\',1)">Mentorship</a></span><br /><br />';
			}
			else
			{	
				echo'<span class="header"> <a href="#StudentBasicForm" onclick="updateInfo(\'StudentBasicForm\',1)">Profile</a></span><br /><br />';
				echo '<div id="separator"></div>';
				echo '<span class="header"> <a href="#StudentBasicForm" onclick="updateInfo(\'StudentBasicForm\',1)">Mentorship</a></span><br /><br />';
			}

			?>
			<div id="separator"></div>
			<span class="header"> <a href="#SuggestionForm" onclick="updateInfo('SuggestionForm',1)">Suggestions</a></span><br /><br />
			<div id="separator"></div>
			<span class="header"> <a href="#ProblemForm" onclick="updateInfo('ProblemForm',1)">Report Bug</a></span><br /><br />
			<div id="separator"></div>
			<span class="header"> <a href="logout.php" >Logout</a></span><br /><br />





		</div>
	


			<div class="divider_small">&nbsp;</div>
			<br />
			<div id="special_links">
				<span class="header">Useful Links</span><br /><br />
				<a href="http://www.iitr.ac.in">IITR Home</a><br />
				<a href="http://people.iitr.ernet.in/thinktank/">Think Tank</a>
				<br />
			</div>
			
		</div>
	</div>
</div>
<hr height="1px" width="960px" color="#cccccc" style="height:1px;"/>
<div id="footer">Credits: <a href="http://www.iitr.ac.in/campus_life/pages/Groups_and_Societies+IMG.html" target="_blank">Information Management Group</a><br/> &copy; Copyright 2010. All Rights Reserved, <a href="http://www.iitr.ac.in/" target="_blank">IIT Roorkee.</a></div>
 <script language="javascript" src="js/image_fader.js"></script>
</body>
</html>

