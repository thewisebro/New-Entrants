<?php
session_start();
require('../connection.php');
if(!isset($_SESSION["student"]))
	header	("Location: ../logout.php");

$username=$_SESSION["student"];

/**************************************Functions**********************************/
require('common.php');
$fields="current_desc,mentor_area,other_mentor_area,aoi,msg_consent";

$where_condition="username='$username'";
$filledInfoArray=retrieveFromDb($dbcon,"student_data",$fields,$where_condition);
$filledInfo=$filledInfoArray[0];

$fullname =returnName($username,$dbconchanneli);

/*********************************************************************************/
?>

<form name="registerForm" method="post" action="student/EditStudentProfilePost.php">
<input type="hidden" name="username" value="<?echo $username;?>">

<span class="header">Welcome <? echo $fullname;?>! You may edit the information you had filled earlier.</span>


<p> <span class="header">*</span> marked  fields are mandatory.</p>

<? ////////////////////////////////////////////////////////////////////////////////////////////////////?>
<fieldset>
<legend>Brief summary of your profile...</legend>
<textarea name="desc" rows="5" cols="50"><? echo $filledInfo['current_desc'];?></textarea> 
<span class="header">*</span></td>
</legend>
</fieldset>

<fieldset>
<legend>Some Questions...</legend>

<? /////////////////////////////////////////////////////////Industry///////////////////////////////////////////////?>

Areas of Interest (separated by commas)<br/>
<input type="text" value="<?echo $filledInfo['aoi'];?>" name="aoi">
<hr/>


<?///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////?>
		I would like to be mentored in the following area(s)<span class="header">*</span><br/>
		<br/>
<?//finding previous choices entered in DB
//This is a bad coding example, I had to do it like this due to lack of time
//whenever you have to add a new checkbox
//define a new variable for it like $edu,$ent etc.
//then check if the string entered in db has it by strpos
//if yes that means you have to show the checkbox as already "checked"

		$edu="";$ent="";$init="";$train="";$employ="";$career="";
		if(!(strpos($filledInfo["mentor_area"],"education")===false)) //triple equal two signs are intentional
			$edu="checked";
		if(!(strpos($filledInfo["mentor_area"],"entrepreneur")===false)) 
			$ent="checked";
		if(!(strpos($filledInfo["mentor_area"],"initial")===false))
			$init="checked";			
		if(!(strpos($filledInfo["mentor_area"],"training")===false))
			$train="checked";
		if(!(strpos($filledInfo["mentor_area"],"employment")===false))
			$employ="checked";
		if(!(strpos($filledInfo["mentor_area"],"career")===false))
			$career="checked";




				

?>
			<input type="checkbox" name="area1" value="education" onchange="if (this.checked) document.getElementById('mentor_area').value+=this.value+'#';else document.getElementById('mentor_area').value=document.getElementById('mentor_area').value.replace('education#','');" <?echo $edu;?>> Furthering Education
		<br/>		
		<input type="checkbox" name="area2" value="entrepreneur" onchange="if (this.checked) document.getElementById('mentor_area').value+=this.value+'#';else document.getElementById('mentor_area').value=document.getElementById('mentor_area').value.replace('entrepreneur#','');" <?echo $ent;?>>Entrepreneurship
		<br/>
		<input type="checkbox" id="area3" value="initial" onchange="if (this.checked) document.getElementById('mentor_area').value+=this.value+'#';else document.getElementById('mentor_area').value=document.getElementById('mentor_area').value.replace('initial#','');" <?echo $init;?>>Initial settling down in the area where I live/work
		<br/>
			<input type="checkbox" id="area4" value="training" onchange="if (this.checked) document.getElementById('mentor_area').value+=this.value+'#';else document.getElementById('mentor_area').value=document.getElementById('mentor_area').value.replace('training#','');" <?echo $train;?>>Finding a place for training (internship)
		<br/>
		<input type="checkbox" id="area5" value="employment" onchange="if (this.checked) document.getElementById('mentor_area').value+=this.value+'#';else document.getElementById('mentor_area').value=document.getElementById('mentor_area').value.replace('employment#','');" <?echo $employ;?>>Finding Employment
                <br/>
		<input type="checkbox" id="area6" value="career" onchange="if (this.checked) document.getElementById('mentor_area').value+=this.value+'#';else document.getElementById('mentor_area').value=document.getElementById('mentor_area').value.replace('career#','');" <?echo $career;?>>Career Development
	 	<br/>

		
	Any Other	
	<input type="text" name="other_mentor_area" value="<? echo $filledInfo['other_mentor_area'];?>" >
		<input type="hidden" id="mentor_area" name="mentor_area" value="<?echo $filledInfo["mentor_area"];?>">
		<hr/>
	

<?/////////////////////////////////////////////////////Mentor Area(s) end here/////////////////////////////////////////////////?>


<? 
		//find out which button is checked as per current choice
		$msg_yes="";$msg_no="";
		if($filledInfo["msg_consent"]=="Yes")
			$msg_yes="checked";
		else
			$msg_no="checked";
?>
		Would you like to receive messages from students/other alumni participating in this programme?
<br/>		<span id="form_tips">The messages will be sent using this portal, your email address will not be disclosed.</span>
<br/>		<input type="radio"  name ="msg_consent" value="Yes" <?echo $msg_yes;?> >Yes<br/>
		<input type="radio" name="msg_consent" value="No" <?echo $msg_no;?>>No



</fieldset><br/>
<input type="hidden" id="notSubmit" value="1">
<input type="submit" value="Submit" onclick="document.getElementById('notSubmit').value=0">
</form>

