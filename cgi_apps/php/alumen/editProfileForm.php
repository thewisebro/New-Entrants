<?php
session_start();
require('connection.php');
if(!isset($_SESSION["username"]))
	header	("Location: logout.php");

$username=$_SESSION["username"];

/**************************************Functions**********************************/
require('common.php');
$fields="company,country,city,state,current_desc,industry,ind_spl,other_ind,mentor_area,num_students,other_mentor_area,aoi,msg_consent";

$where_condition="username='$username'";
$filledInfoArray=retrieveFromDb($dbcon,"mentor_data",$fields,$where_condition);
$filledInfo=$filledInfoArray[0];
/*********************************************************************************/
?>




<form name="registerForm" method="post" action="editProfilePost.php">
<input type="hidden" name="username" value="<?echo $username;?>">

<span class="header">Welcome <? echo $username;?>! You may edit the information you had filled in <u>Step 2</u> here</span>


<p> <span class="header">*</span> marked  fields are mandatory.</p>
<fieldset>
	<legend>Where are you nowadays...</legend>
		<table border="0">
			<tr>
			<td>Company/Institute</td>
			<td><input type="text" name="company" value="<? echo $filledInfo['company'];?>"></td>
			</tr>

			
			<tr>
			<td>City</td>
			<td><input type="text" name="city" value="<? echo $filledInfo['city'];?>"></td>
			</tr>
			<tr>
			<td>State</td>
			<td><input type="text" name="state" value="<? echo $filledInfo['state'];?>"></td>
			</tr>
		
			<tr>
			<td>Country</td>

			<td><a href="javascript:;" onclick="this.style.display='none';document.getElementById('countryList').style.display='inline';document.getElementById('updated_country').value='None';" class="editable">
<? 
$countryArray=retrieveFromDb($dbcon,"codes_used","value","code='".$filledInfo['country']."'");
$country=$countryArray[0];
echo $country['value'];?> [Edit]</a><div id="countryList" style="display:none"><? include 'countryList.php'; ?> </div></td>
		
	<input type="hidden" name="updated_country" value="<? echo $filledInfo['country'];?>" id="updated_country">




			</tr>
			
				</table>
	</legend>
</fieldset>
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
		Industry<span class="header">*</span> <br/>
<a href="javascript:;" onclick="this.style.display='none';document.getElementById('industry_lst').style.display='inline';document.getElementById('updated_industry').value='None';document.getElementById('updated_ind_spl').value='None';document.getElementById('updated_other_ind').value='None';" class="editable"><?

	$codeValueArray=retrieveFromDb($dbcon,"codes_used","value","code='".$filledInfo['industry']."'");
	$codeValue=$codeValueArray[0];

echo $codeValue['value'].">".$filledInfo['ind_spl'];


?> &nbsp;[Edit]</a>
		
		<div id="industry_lst" style="display:none"><? include 'industryList.php';?>	</div>
		<input type="hidden" name="updated_industry" id="updated_industry" value="<?echo $filledInfo['industry'];?>">
	
		<input type="hidden" name="updated_ind_spl" id="updated_ind_spl" value="<?echo $filledInfo['ind_spl'];?>">

		<input type="hidden" name="updated_other_ind" id="updated_other_ind" value="<?echo $filledInfo['other_ind'];?>">
		<hr/>
	
<?/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////?>

Areas of Interest (separated by commas)<br/>
<input type="text" value="<?echo $filledInfo['aoi'];?>" name="aoi">
<hr/>


<?///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////?>
		I would like to mentor a student in the following area(s)<span class="header">*</span><br/>
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



		Maximum number of students I would like to mentor<span class="header">*</span>
		<a href="javascript:;" onclick="this.style.display='none';document.getElementById('opt_list').style.display='inline';document.getElementById('updated_num_students').value='None';" class="editable"><?echo $filledInfo['num_students'];?> &nbsp;[Edit]</a>
	

		<input type="hidden" name="updated_num_students" id="updated_num_students" value="<?echo $filledInfo['num_students'];?>">
	

		<div id="opt_list" style="display:none">
		<select name="num_students">
			<option value="">Select...</option>
			<option value="2">2</option>
			<option value="3">3</option>
			<option value="4">4</option>
			<option value="5">5</option>
		</select>
		</div>

	<hr/>

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

