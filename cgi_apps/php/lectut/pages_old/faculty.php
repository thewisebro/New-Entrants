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
	header("Location: ../pages/final_student.php");
}

?>

<html>
<head>
<title>Lectures and Tutorials</title>

<link rel=stylesheet href="../styles_old/lectntut.css" type="text/css">
	<script src="../common/jscriptfunc.js"></script>



</head>

<body>
<div id="container">

	<div id="top_links">

<?php
if($loggedIn && $_SESSION['group']=='f')
{
		disp_fac_design_choice($loggedIn,$facId);
}
?>
		<div class="curve_edge_lt">&nbsp;</div>
		<div class="link"><a href="/" target="_blank">Channel I</a></div>
		<div class="curve_edge_rt"><a href="mailto:img@iitr.ernet.in" target="_blank"></a></div>
		<div class="curve_edge_lt">&nbsp;</div>
		<div class="link"><a href="mailto:img@iitr.ernet.in" target="_blank">Complaints/Suggestions</a></div>
		<div class="curve_edge_rt"><a href="mailto:img@iitr.ernet.in" target="_blank"></a></div>
		<div class="curve_edge_lt"></div>
		<div class="link"><a href="/nucleus/logout">Logout</a></div>
		<div class="curve_edge_rt"></div>
	</div>
	<!---Top Links div end here-->

	
	<div id="header_links">
		<div id="header">&nbsp;</div>
		<div id="links_right">
		<div class="links"><a href="faculty.php">Upload lectures and tutorials</a></div>
		<div class="links"><a href="managefiles.php">Manage files</a></div>
		<div class="links"><a href="dept_list.php">View &nbsp;&nbsp; lectures and tutorials</a></div>
		</div>	
	</div>

	<!--Header ends here-->

	<?php
		database::connectToDatabase();
		$facName=mysql_fetch_array(database::executeQuery(database::getFacName($facId)));
		database::closeDatabase();

	?>

	<div id="running_text2">
	<div id="running_text_header">Welcome <?echo $facName[0];?></div>

	


		<div id="middle_text">Please note: <br />
			<ul id="list_faculty">
				<li>Maximum allowed filesize for upload is 10 MB. (Tip: Instead of Uploading *.ppt(powerpoint presentation) upload only the Slideshow (*.pps).This option is available in File->Save As->Powerpoint Show. This reduces file size.)</li>
				<li>The filenames should preferably contain only letters and numbers (no special characters like ', !, *,/etc.).</li>
				<li>Before uploading make sure that the filename shown in the 'Upload File' textbox is the same as the name of the file that exists on your system.</li>
				<li>Kindly limit the filename upto 100 characters, by first renaming it on your system itself.</li>
				<li>In case of any problems in accessing or using this application please let us know - <a href="mailto:img@iitr.ernet.in">Complaints/ Suggestions</a></li>


			</ul>
			<br />

		</div>
	
	<!--Runing text ends here-->

		
	<!--upload box starts here-->
	<?php
	$temp=$_GET['temp1'];
	if(isset($temp))
	{
			$logfile=fopen("../lectut_profs_logs.txt",'a');
			$logstring="";

			print "<span class=\"statusMsg\">";
			if($temp=='y'){
        	        print "File is successfully uploaded.You can view the changes from given link: \n";
                        print "<a href='managefiles.php'>"."View Changes"."</a>";
 			$logstring=(string)date("D F d Y",time())." ".(string)$facId." temp=y File uploaded\n"; 	

 			}
                	else if($temp=='e'){
       			print "This file has already been uploaded by you. Please upload other file.";
			$logstring=date("D F d Y",time())." ".$facId." temp=e File already exists\n"; 	

			}
			else if($temp=='n'){
			print "File not uploaded. Please try again after some time..";
			$logstring=date("D F d Y",time())." ".$facId." temp=n File  not uploaded. Please try after some time.\n"; 	
  
			}else if($temp=='u'){
                        print "Please select the file.";
			$logstring=date("D F d Y",time())." ".$facId." temp=u Please select the file.\n"; 	

			}	
			else{
				print "Please select a choice.";
			$logstring=date("D F d Y",time())." ".$facId." temp=else Please select a choice.\n"; 	

			}
			print "</span>";
			fwrite($logfile,$logstring);
			fclose($logfile);
	}
	?>
		<div id="middle_upload">
			<div class="upload_lecture">
			
			<form method="post" enctype="multipart/form-data" name="upload" action="upload.php" onsubmit="return validate_upload_form();">
			<input type="hidden" name="type" value="lec">
			<input type="hidden" name="fac_id" value="<?php echo $facId; ?>">
			<div class="upload">Subject code:&nbsp;&nbsp;&nbsp;<input type="text" class="text_box" name="subcode" /></div>
			<div class="upload">Topic/Chapter:&nbsp;<input type="text" class="text_box" name="topic" /></div>
			<div class="upload"><br />Upload file:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--<input type="text" class="text_box" />-->
			</div>
			<div id="maximum_size"><!--(Max. allowed filesize :10MB)-->
			<input type="file" name="file">		
	
			<!--<div id="widthify">Permissions&nbsp;&nbsp;&nbsp;&nbsp;</div>
			<select name="permission">
			<option value="false">All</option>
			<option value="true">Only Registered</option>
			</select><br>-->

			<br /><br />	
			(Max. filesize :10MB)

			<input type="image" src="../styles_old/images/upload_button_lec.gif" class="upload_button"></div>

			</form>
			</div>

			<div class="upload_lecture">
			
			<form method="post" enctype="multipart/form-data" name="upload" action="upload.php" onsubmit="return validate_upload_form();">
			<input type="hidden" name="type" value="tut">
			<input type="hidden" name="fac_id" value="<?php echo $facId; ?>">
			<div class="upload">Subject code:&nbsp;&nbsp;&nbsp;<input type="text" class="text_box" name="subcode" /></div>
			<div class="upload">Topic/Chapter:&nbsp;<input type="text" class="text_box" name="topic" /></div>
			<div class="upload"><br />Upload file:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--<input type="text" class="text_box" />-->
			</div>
			<div id="maximum_size"><!--(Max. allowed filesize :10MB)-->
			<input type="file" name="file">		
	
			<!--<div id="widthify">Permissions&nbsp;&nbsp;&nbsp;&nbsp;</div>
			<select name="permission">
			<option value="false">All</option>
			<option value="true">Only Registered</option>
			</select><br>-->

			<br /><br />	
			(Max. filesize :10MB)

			<input type="image" src="../styles_old/images/upload_button_tut.gif" class="upload_button"></div>

			</form>
			</div>
		</div>		
		<!--Upload lectures box ends here-->
		
		<div id="middle_upload_2">
			<div class="upload_lecture">
			
			<form method="post" enctype="multipart/form-data" name="upload" action="upload.php" onsubmit="return validate_upload_form();">
			<input type="hidden" name="type" value="exam">
			<input type="hidden" name="fac_id" value="<?php echo $facId; ?>">
			<div class="upload">Subject code:&nbsp;&nbsp;&nbsp;<input type="text" class="text_box" name="subcode" /></div>
			<div class="upload">Topic/Chapter:&nbsp;<input type="text" class="text_box" name="topic" /></div>
<!--			<div class="upload">Year:&nbsp;<input type="text" name="year" class="text_box" value=""></div>-->
			<div class="upload"><br />Upload file:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--<input type="text" class="text_box" />-->
			</div>
			<div id="maximum_size"><!--(Max. allowed filesize :10MB)-->
			<input type="file" name="file">		
	
			<!--<div id="widthify">Permissions&nbsp;&nbsp;&nbsp;&nbsp;</div>
			<select name="permission">
			<option value="false">All</option>
			<option value="true">Only Registered</option>
			</select><br>-->

			<br /><br />	
			(Max. filesize :10MB)

			<input type="image" src="../styles_old/images/upload_button_exam.gif" class="upload_button"></div>

			</form>
			</div>

			<div class="upload_lecture">
			
			<form method="post" enctype="multipart/form-data" name="upload" action="upload.php" onsubmit="return validate_upload_form();">
			<input type="hidden" name="type" value="soln">
			<input type="hidden" name="fac_id" value="<?php echo $facId; ?>">
			<div class="upload">Subject code:&nbsp;&nbsp;&nbsp;<input type="text" class="text_box" name="subcode" /></div>
			<div class="upload">Topic/Chapter:&nbsp;<input type="text" class="text_box" name="topic" /></div>
			<div class="upload"><br />Upload file:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--<input type="text" class="text_box" />-->
			</div>
			<div id="maximum_size"><!--(Max. allowed filesize :10MB)-->
			<input type="file" name="file">		
	
			<!--<div id="widthify">Permissions&nbsp;&nbsp;&nbsp;&nbsp;</div>
			<select name="permission">
			<option value="false">All</option>
			<option value="true">Only Registered</option>
			</select><br>-->

			<br /><br />	
			(Max. filesize :10MB)

			<input type="image" src="../styles_old/images/upload_button_soln.gif" class="upload_button"></div>

			</form>
			</div>
		</div>		

		<!--Right side of middle_banner ends here-->	
			
		
			
	
</div> </div>		

		<div id="footer">
			<div id="footer_text">
			<div id="bottom_curve_lt">&nbsp;</div>
			<div id="img">Credits: <a href="http://www.iitr.ernet.in/campus_life/pages/Groups_and_Societies+IMG.html" target="_blank">Information Management Group</a></div>
			
			<div id="bottom_curve_rt">&nbsp;&nbsp;</div>
			</div>
		</div>
		<!--Footer ends here-->

 <script type="text/javascript" src="/static/js/piwik.js"></script>
</body>  
</html>

