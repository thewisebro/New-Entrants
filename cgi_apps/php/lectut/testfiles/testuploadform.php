<?php
/*session_start();
if(!session_is_registered(username))
{
	header("Location: index.php?temp=p");
}*/
$facId="padamfec";
//$facId=$_SESSION['username'];
?>
<html>
	<head>
	<title>Lectures and Tutorials</title>
	<script type="text/javascript" src="testjscript.js"></script>
	</head>
 	<body onLoad="show_form()">
<?php
/*echo "<a href=logout.php?".session_name()."=".session_id().">Logout</a><br>";
echo "<a href=dept_list.php?".session_name()."=".session_id().">Browse All</a><br>";
echo "<a href=managefiles.php?".session_name()."=".session_id().">Manage Files</a><br>";
*/
?>
	<div id="resultUpload">
<?php
	$temp=$_GET['temp'];
	if(isset($temp))
	{
		if($temp=='y')
			print("File uploaded.");
		elseif($temp=='e')
			print("File already exists.");
		elseif($temp=='n')
			print("File not uploaded. Please try after some time.");
		elseif($temp='u')
			print("Please select the file");
		else
			print("Please select a choice.");
	}
?>
	</div>
	<div id="uploadFormMain">
		<form method="post" enctype="multipart/form-data" name="upload" action="pages/upload.php">
			Select Type&nbsp;&nbsp;&nbsp;
			<select name="type" onChange="show_form_special(document.upload.type.value)">
			<option value="lec">Lecture</option>
			<option value="tut">Tutorial</option>
			<option value="exam">Exam Paper</option>
			<option value="soln">Solution</option>
			</select><br>		
			<input type="hidden" name="fac_id" value=<? echo $facId; ?>><br>
			Subject Code&nbsp;&nbsp;
			<input type="text" name="subcode"><br>
			Select File&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			<input type="file" name="file"><br>
			Topic&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			<input type="text" name="topic"><br>
			Permissions&nbsp;&nbsp;&nbsp;&nbsp;
			<select name="permission">
				<option value="false">All</option>
				<option value="true">Only Registered</option>
			</select><br>
	<div id="show_exam_year">
			Year&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			<input type="text" name="year" value=""><br>
	</div>
	<div id="show_soln_link">
			Link&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			<input type="text" name="link" value=""><br>
	</div>
			<input type="submit" value="Upload" onclick="javascript:uploadAjax(this.form)>&nbsp;
			<input type="reset" value="Reset">
		</form>
	</div>
	<input type="button" id="addAnotherFile" value="Upload Another File" onClick="show_form()">
	</body>
</html>

