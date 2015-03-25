<?php
session_start();
if(!isset($_SESSION["student"]))
	die("Either you are not logged in or your session has expired.");

$username=$_SESSION["student"];
?>

<form name="registerForm" method="post" action="student/StudentBasicRegister.php" onsubmit="return checkFullForm(this);">
<input type="hidden" name="username" value="<?echo $username;?>">
<?
	include("../connection.php");
	include("common.php");
	
	$fullname =returnName($username,$dbconchanneli);

	include("../disconnection.php");
?>
<span class="header">Welcome <? echo $fullname;?>, your profile:-</span>

<p><b>Note:</b><ul><li>You may edit the following information later by logging into this portal again.</li><li>You need to fill this form before you can browse the other features of this application.</li></ul></p>

<p> <span class="header">*</span> marked  fields are mandatory.</p>

<?
if($Photo)
{
if ($_FILES["Photo"]["error"] > 0)
  {
    echo "Error: " . $_FILES["Photo"]["error"] . "<br />";
      }

      else
      {
      $filename=$_FILES['Photo']['name'];
      $filelocation=$_FILES['Photo']['tmp_name'];
      $filesize_byte=$_FILES['Photo']['size'];
      $filesize=$filesize_byte/1024;
      $ext=pathinfo($_FILES['Photo']['name']);
      $fileext=$ext['extension'];
      //echo "<script language='javascript'>alert('File size is $filesize kb.')</script>";
      $filetype=$_FILES['Photo']['type'];
      //echo "<script language='javascript'>alert('File type is $filetype.')</script>";
      $uploaddir="uploads/".$username.".".$fileext;
      //echo "<script type=text/javascript>alert('$fileext')</script>";
      if($filesize>=25.00||($filetype!='image/jpeg' && $filetype!='image/gif' && $filetype!='image/png'))
      {
      echo "<script language='javascript'>alert('Can not submit. Either too big file or not a valid photo. File must be in jpeg, gif or png format less than 25 KB in size.')</script>";
      }
      else
      {
      move_uploaded_file($filelocation,$uploaddir);
      $query=pg_query("UPDATE basic_data SET photosrc='$username.$fileext' where username='$username'");
      //header("Location: http://192.168.121.2/php/AluMen/loginSuccess.php");
      }
      }
      }
      else
      {

      //echo "<script language='javascript'>alert('No photo chosen.')</script>";

      }
      include('BasicProfile.php');
?>


<fieldset>
<legend>Brief summary of your profile...</legend>
		<textarea name="desc" rows="5" cols="50" onclick="if(this.value=='Anything you would like to share with an alumni whom you would like to be mentored by...')this.value=''">Anything you would like to share with an alumni whom you would like to be mentored by...</textarea> <span class="header">*</span></td>
</legend>
</fieldset>

<fieldset>
<legend>Some Questions...</legend>

		<hr/>
		Areas of Interest (separated by commas)
		<br/>
		
		<input type="text" name="aoi">

		<hr/>
		I would like to be mentored in the following area(s)<br/>
		<br/>
		<input type="checkbox" name="area1" value="education" onchange="if (this.checked) document.getElementById('mentor_area').value+=this.value+'#'"> Furthering Education
		<br/>		
		<input type="checkbox" name="area2" value="entrepreneur" onchange="if (this.checked) document.getElementById('mentor_area').value+=this.value+'#'">Entrepreneurship
		<br/>
		<input type="checkbox" id="area3" value="initial" onchange="if (this.checked) document.getElementById('mentor_area').value+=this.value+'#'">Initial settling down in the area where I live/work
		<br/>
		<input type="checkbox" id="area4" value="training" onchange="if (this.checked) document.getElementById('mentor_area').value+=this.value+'#'">Finding a place for training (internship)
		<br />
		<input type="checkbox" id="area5" value="employment" onchange="if (this.checked) document.getElementById('mentor_area').value+=this.value+'#'">Finding Employment
		<br />
		<input type="checkbox" id="area6" value="career" onchange="if (this.checked) document.getElementById('mentor_area').value+=this.value+'#'">Career Development


		

		<br/>
		<input type="hidden" id="mentor_area" name="mentor_area" value="">
	<br/>Any other
	<input type="text" name="other_mentor_area" value=""  >
		
		<hr/>
		Upload your recent photograph:<br/>
		<input type="file" name="photo"><span id="form_tips">(only JPEG with maximum size limit of 25kB allowed)</span></td>
		
		<hr/>
		Would you like to receive messages from alumni/ other students participating in this programme?
<br/>		<span id="form_tips">The messages will be sent using this portal, your email address will not be disclosed.</span><br/>
		<input type="radio" name ="msg_consent" value="Yes">Yes<br/>
		<input type="radio" name="msg_consent" value="No">No

</fieldset><br/>
<input type="hidden" id="notSubmit" value="1">
<input type="submit" value="Submit" onclick="document.getElementById('notSubmit').value=0">
</form>

