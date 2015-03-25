<?php
session_start();
include_once('connection.php');
if(!isset($_SESSION["username"]))
{
	header("location: logout.php");


}
$username=$_SESSION["username"];

/**************************************Functions**********************************/
require('common.php');

$fields="company,country,city,state,current_desc,industry,ind_spl,other_ind,mentor_area,num_students,other_mentor_area,aoi,msg_consent";

$where_condition="username='$username'";
$filledInfoArray=retrieveFromDb($dbcon,"mentor_data",$fields,$where_condition);
$filledInfo=$filledInfoArray[0];

$fields="enrollment_no,fullname,email,department,degree,passing_year,photosrc";

$where_condition="username='$username'";
$basicInfoArray=retrieveFromDb($dbcon,"basic_data",$fields,$where_condition);
$basicInfo=$basicInfoArray[0];



/*********************************************************************************/
?>




<span class="header">Welcome <? echo $username;?>!<br/>
You are now logged in.</span> You may edit the information displayed below by clicking here <span class="header"><a href='#EditProfileForm' onclick='updateInfo("EditProfileForm",1)'>[Edit Profile]</a></span>


<fieldset>
<legend>Basic Details</legend>
		<table border="0">
		<tr>
		<td><img height=150px" width="150px" src="<? if($basicInfo['photosrc']==NULL)echo "images/default.JPG";else echo $basicInfo['photosrc'];?>" alt="photo" /></td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>
		<table border="0">
			<tr>
			<td><b>Full Name</b></td>
			<td><? echo $basicInfo['fullname'];?></td>
			</tr>
			
			<tr>
			<td><b>Enrollment no.</b></td>
			<td><? echo $basicInfo['enrollment_no'];?></td>
			</tr>
	
			<tr>
			<td><b>Email</b></td>
			<td><? echo $basicInfo['email'];?></td>
			</tr>

			<tr>
			<td><b>Password</b></td>
			<td><a href="#ChangePasswordForm" onclick="updateInfo('ChangePasswordForm',1)"><span class="header">Change Password</span></a></td>
			</tr>

		</table>
		</td>
		</tr>

<tr><td><a href="#New" onclick="updateInfo('ChangePhoto',1)" >Change Photo</a></td></tr>
		</table>
</fieldset>




<fieldset>
	<legend>Where are you nowadays...</legend>
		<table border="0">
			<tr>
			<td><b>Company/Institute</b></td>
			<td><? echo $filledInfo['company'];?></td>
			</tr>

			<tr>
			<td><b>City</b></td>
			<td><?echo $filledInfo['city'];?></td>
			</tr>
		
			<tr>
			<td><b>State</b></td>
			<td><?echo $filledInfo['state'];?></td>
			</tr>
			
			
				
			<tr>
			<td><b>Country</b></td>

			<td>
<? 
$countryArray=retrieveFromDb($dbcon,"codes_used","value","code='".$filledInfo['country']."'");
$country=$countryArray[0];
echo $country['value'];?> </td>
		




			</tr>
			
		</table>
	</legend>
</fieldset>

<fieldset>
<legend>Brief summary of your profile...</legend>
<p><? echo $filledInfo['current_desc'];?></p></td>
</legend>
</fieldset>

<fieldset>
<legend>Some Questions...</legend>
<b>Industry</b><br/>
<?
	$codeValueArray=retrieveFromDb($dbcon,"codes_used","value","code='".$filledInfo['industry']."'");
$codeValue=$codeValueArray[0];
echo $codeValue['value'].">".$filledInfo['ind_spl'];


?>
		
		<hr/>
<b>Areas of Interest</b><br/>
<?echo $filledInfo["aoi"];?>



<hr/>
		<b>I would like to mentor a student in the following area(s)</b><br/>
<? 
$filledInfo["mentor_area"]=str_replace("#",",",$filledInfo['mentor_area']);
$filledInfo["mentor_area"]=str_replace("education","Furthering education",$filledInfo['mentor_area']);
$filledInfo["mentor_area"]=str_replace("entrepreneur","Entrepreneurship",$filledInfo['mentor_area']);
$filledInfo["mentor_area"]=str_replace("initial","Initial settling down in the area I live/work",$filledInfo['mentor_area']);
echo $filledInfo["mentor_area"].$filledInfo["other_mentor_area"];
?>
		<hr/>
	<b>Number of students I would like to mentor</b><br/>
	<? echo $filledInfo["num_students"];?>	
	<hr/>
		<b>Would you like to receive messages from students/other alumni participating in this programme?</b>
	<br/>	<span id="form_tips">The messages will be sent using this portal, your email address will not be disclosed.</span><br/>
		<?echo $filledInfo['msg_consent'];?>
	
</fieldset><br/>

