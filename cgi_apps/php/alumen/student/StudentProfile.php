<?php
//header("Expires: Mon, 26 Jul 1997 05:00:00 GMT");
//header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
//header("Cache-Control: no-store, no-cache, must-revalidate");
//header("Cache-Control: post-check=0, pre-check=0", false);
//header("Pragma: no-cache");
error_reporting(E_ALL);
ini_set("display_errors",1);

session_start();
include_once('../connection.php');
if(!isset($_SESSION["username"]))
{
	header("location: ../logout.php");
}
$alumni=$_SESSION['username'];
$student=$_SESSION["viewstudent"];

/**************************************Functions**********************************/
require('common.php');

$status_al = getStudentStatus_Al($alumni,$student,$dbcon);
if((($status_al=='A+')||($status_al=='F'))&&($status_al!=0))
	$viewing_rights=1;
else
	$viewing_rights=0;

$fields="current_desc,mentor_area,other_mentor_area,aoi,msg_consent,photosrc";
$where_condition="username='$student'";
$filledInfoArray=retrieveFromDb($dbcon,"student_data",$fields,$where_condition);
if(count($filledInfoArray)!=0)
	$filledInfo = $filledInfoArray[0];
else
{	
	$filledInfo['current_desc']=NULL;
	$filledInfo['mentor_area']="-";
	$filledInfo['other_mentor_area']="-";
	$filledInfo['aoi']="-";
	$filledInfo['msg_consent']="Yes";
	$filledInfo['photosrc']=NULL;
}
$fields = " auth.username as enrollment_no, nperson.name as name, nperson.email_id as alternate_email, nbranch.name as discipline_full, nbranch.degree as degree"; //add course here

$basicInfoArray = getStudentDetails($dbconchanneli, $fields, $username);
$basicInfo = $basicInfoArray[0];

function codeValue($dbcon, $code) {
	$value=retrieveFromDb($dbcon,"codes_used","value","code='$code'");
	return $value[0][0];
}


/*********************************************************************************/
?>

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
	
    	<? if($viewing_rights==1)
		   {
		    echo "	
					<tr>
					<td><b>Enrollment no.</b></td>
					<td>".$basicInfo['enrollment_no']."</td>
					</tr>
	
					<tr>
					<td><b>Email</b></td>
					<td>".$basicInfo['alternate_email']."</td>";
		   }
		 ?>

			<tr>
			<td><b>Class</b></td>
			<td><? echo $basicInfo['degree']; echo " (".codeValue($dbcon, $basicInfo['course']).")"; ?></td>
			</tr>
		 
		 <? if($viewing_rights==1)
		    {
		     echo "
					<tr>
					<td><b>Branch</b></td>
					<td>".$basicInfo['discipline_full'])."</td>
					</tr>";
			}
		 ?>

		</table>
		</td>
		</tr>

		<tr>
			<td><center><a href="#New" onclick="document.getElementById('changePhotoForm').style.display='block';"><span class="header">Change Photo</span></a></center></td>
		</tr>
		<tr>
			<td colspan="5">
				<div id="changePhotoForm" style="display:none">
					<form action="loginSuccess.php" method="post" enctype="multipart/form-data">
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

