<?php
//header("Expires: Mon, 26 Jul 1997 05:00:00 GMT");
//header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
//header("Cache-Control: no-store, no-cache, must-revalidate");
//header("Cache-Control: post-check=0, pre-check=0", false);
//header("Pragma: no-cache");

session_start();
include_once('../connection.php');
if(!isset($_SESSION["student"]))
{
	header("location: ../logout.php");
}
$username=$_SESSION["student"];


if(isset($_SESSION['message']))
{
        echo $_SESSION['message']."<br/><br />";
	unset($_SESSION['message']);
}

/**************************************Functions**********************************/
include_once('common.php');

$fields="current_desc,mentor_area,other_mentor_area,aoi,msg_consent,photosrc";
$where_condition="username='$username'";
$filledInfoArray=retrieveFromDb($dbcon,"student_data",$fields,$where_condition);
$filledInfo = $filledInfoArray[0];


$fields = " auth.username as enrollment_no, nperson.name as name, nperson.email_id as alternate_email, nbranch.name as discipline_full, nbranch.degree as degree"; //add course here

$basicInfoArray = getStudentDetails($dbconchanneli, $fields, $username);
$basicInfo = $basicInfoArray[0];
function codeValue($dbcon, $code) {
	$value=retrieveFromDb($dbcon,"codes_used","value","code='$code'");
	return $value[0][0];
}


/*********************************************************************************/
?>




<span class="header">Welcome <? echo $basicInfo['name'];?>!<br/>
You are now logged in.</span> You may edit the information displayed below by clicking here <span class="header"><a href='#EditStudentProfileForm' onclick='updateInfo("EditStudentProfileForm",1)'>[Edit Profile]</a></span>

<fieldset>
<legend>Basic Details</legend>
		<table border="0">
		<tr>
		<td><img height=150px" width="150px" src="<? if($filledInfo['photosrc']==NULL)echo "images/default.JPG";else echo $filledInfo['photosrc'];?>" alt="photo" /></td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>
		<table border="0">
			<tr>
			<td><b>Name</b></td>
			<td><? echo $basicInfo['name'];?></td>
			</tr>
			
			<tr>
			<td><b>Enrollment no.</b></td>
			<td><? echo $basicInfo['enrollment_no'];?></td>
			</tr>
	
			<tr>
			<td><b>Email</b></td>
			<td><? echo $basicInfo['alternate_email'];?></td>
			</tr>

			<tr>
			<td><b>Class</b></td>
			<td><? echo $basicInfo['degree']; //echo " (".codeValue($dbcon, $basicInfo['course']).")"; ?></td>
			</tr>

			<tr>
			<td><b>Branch</b></td>
			<td><? echo $basicInfo['discipline_full'] ?></td>
			</tr>

			<tr>
			<td><b>Password</b></td>
			<td><a href="http://192.168.121.26:81" target="_blank"><span class="header">Change Password</span></a></td>
			</tr>

		</table>
		</td>
		</tr>

		<tr>
			<td><center><a href="#New" onclick="document.getElementById('changePhotoForm').style.display='block';"><span class="header">Change Photo</span></a></center></td>
		</tr>
		<tr>
			<td colspan="5">
				<div id="changePhotoForm" style="display:none">
					<form action="student.php" method="post" enctype="multipart/form-data">
					<input type="file" name="Photo" id="Photo"/><input type="submit" name="DoSubmit" value="Submit" />
					</form>
					<button onClick="document.getElementById('changePhotoForm').style.display='none';">Cancel</button>
				</div>

			</td>
		</tr>
		</table>
</fieldset>

<fieldset>
<legend>Brief summary of your profile...</legend>
<p><? echo $filledInfo['current_desc'];?></p></td>
</legend>
</fieldset>

<fieldset>
<legend>Some Questions...</legend>
		
		<hr/>
<b>Areas of Interest</b><br/>
<?echo $filledInfo["aoi"];?>



<hr/>
		<b>I would like to be mentored in the following area(s)</b><br/>
<? 
$filledInfo["mentor_area"]=str_replace("#",",",$filledInfo['mentor_area']);
$filledInfo["mentor_area"]=str_replace("education","Furthering education",$filledInfo['mentor_area']);
$filledInfo["mentor_area"]=str_replace("entrepreneur","Entrepreneurship",$filledInfo['mentor_area']);
$filledInfo["mentor_area"]=str_replace("initial","Initial settling down in the area I live/work",$filledInfo['mentor_area']);
$filledInfo["mentor_area"]=str_replace("training","Finding a place for training (internship)",$filledInfo['mentor_area']);
$filledInfo["mentor_area"]=str_replace("employment","Finding Employment",$filledInfo['mentor_area']);
$filledInfo["mentor_area"]=str_replace("career","Career Development",$filledInfo['mentor_area']);

echo $filledInfo["mentor_area"].$filledInfo["other_mentor_area"];
?>
	<hr/>
		<b>Would you like to receive messages from students/other alumni participating in this programme?</b>
	<br/>	<span id="form_tips">The messages will be sent using this portal, your email address will not be disclosed.</span><br/>
		<?echo $filledInfo['msg_consent'];?>
	
</fieldset><br/>

