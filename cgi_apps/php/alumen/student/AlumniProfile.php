<?php
//header("Expires: Mon, 26 Jul 1997 05:00:00 GMT");
//header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
//header("Cache-Control: no-store, no-cache, must-revalidate");
//header("Cache-Control: post-check=0, pre-check=0", false);
//header("Pragma: no-cache");
error_reporting(0);
//ini_set("display_errors",1);

session_start();
include_once('../connection.php');

if(!isset($_SESSION["student"]))
{
	header("location: logout.php");
}

$username=$_SESSION['alumni'];

/**************************************Functions**********************************/
require('common.php');

$status_al = getStudentStatus_Al($username,$_SESSION['student'],$dbcon);
if(($status_al=='Approved')||($status_al=='Finalized'))
	$viewing_rights=1;
else
	$viewing_rights=0;

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
                         <td><b>Company/Institute</b></td>
                         <td><? echo $filledInfo['company'];?></td>
                 </tr>
		
		<? if($viewing_rights==1)
		   {
		    echo "	<tr>
				<td><b>Enrollment no.</b></td>
				<td>".$basicInfo['enrollment_no']."</td>
				</tr>
	
		";
		   }
		 ?>
			</tr> 

		</table>
		</td>
		</tr>

		</table>
</fieldset>



<? if($viewing_rights==1){?>

<fieldset>
	<legend>Where are you nowadays...</legend>
		<table border="0">
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
echo $country['value']."</td>";
}
?>
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
$filledInfo["mentor_area"]=str_replace("training","Finding a place for training (internship)",$filledInfo['mentor_area']);
$filledInfo["mentor_area"]=str_replace("employment","Finding Employment",$filledInfo['mentor_area']);
$filledInfo["mentor_area"]=str_replace("career","Career Development",$filledInfo['mentor_area']);

echo $filledInfo["mentor_area"].$filledInfo["other_mentor_area"];
?>
		<hr/>
	<b>Number of students I would like to mentor</b><br/>
	<? echo $filledInfo["num_students"];?>	
	<hr/>
	
</fieldset><br/>

