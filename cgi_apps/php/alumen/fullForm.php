<?php
session_start();
if(!isset($_SESSION["username"]))
	die("Either you have not yet completed Step 1 or your session has expired.");

$username=$_SESSION["username"];
?>

<form name="registerForm" method="post" action="fullRegister.php" onsubmit="return checkFullForm(this);">
<input type="hidden" name="username" value="<?echo $username;?>">

<span class="header">Welcome <? echo $username;?>! You have completed Step 1. <br/>Step 2 of 2 : Your Profile</span>

<p><b>Note:</b> You may edit the following information later by logging into this portal again.</p>

<p> <span class="header">*</span> marked  fields are mandatory.</p>
<fieldset>
	<legend>Where are you nowadays...</legend>
		<table border="0">
			<tr>
			<td>Company/Institute/Organization</td>
			<td><input type="text" name="company"></td>
			</tr>

			<tr>
			<td>City</td>
			<td><input type="text" name="city"></td>
			</tr>
			<tr>
			<td>State (Area)</td>
			<td><input type="text" name="state"></td>
			</tr>


				
			<tr>
			<td>Country</td>
			<td><? include 'countryList.php'; ?> </td>
			</tr>
			
					</table>
	</legend>
</fieldset>

<fieldset>
<legend>Brief summary of your profile...</legend>
		<textarea name="desc" rows="5" cols="50" onclick="if(this.value=='Anything you would like to share with a student whom you would like to mentor...')this.value=''">Anything you would like to share with a student whom you would like to mentor...</textarea> <span class="header">*</span></td>
</legend>
</fieldset>

<fieldset>
<legend>Some Questions...</legend>
		Industry<span class="header">*</span> <br/>
		<? include 'industryList.php';?>		


		<hr/>
		Areas of Interest (separated by commas)
		<br/>
		
		<input type="text" name="aoi">




		<hr/>
		I would like to mentor a student in the following area(s)<br/>
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
		Maximum number of students I would like to mentor<span class="header">*</span>
		<select name="num_students">
			<option value="">Select...</option>
			<option value="2">2</option>
			<option value="3">3</option>
			<option value="4">4</option>
			<option value="5">5</option>
		</select>

		<hr/>
		Would you like to receive messages from students/other alumni participating in this programme?
<br/>		<span id="form_tips">The messages will be sent using this portal, your email address will not be disclosed.</span><br/>
		<input type="radio" name ="msg_consent" value="Yes">Yes<br/>
		<input type="radio" name="msg_consent" value="No">No

</fieldset><br/>
<input type="hidden" id="notSubmit" value="1">
<input type="submit" value="Submit" onclick="document.getElementById('notSubmit').value=0">
</form>

