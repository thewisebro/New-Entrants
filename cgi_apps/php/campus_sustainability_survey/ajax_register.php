<?php
	require('common.php');
  $email=$_SESSION['email'];
	if(true){
		$acad_year='';
		$cat_details='';
		$cat_type='';
		$category=mysql_real_escape_string($_POST['category']);
		if($category=='student'){
			$cat_type=mysql_real_escape_string($_POST['acad_year']);
			$cat_details=mysql_real_escape_string($_POST['student_category']);
		}
		else if($category=='nonacademic'){
			$cat_details=mysql_real_escape_string($_POST['nonacademic_designation']);
			$cat_type=mysql_real_escape_string($_POST['nonacademic_category']);
		}	
		$gender=mysql_real_escape_string($_POST['sex']);
		$age=mysql_real_escape_string($_POST['age']);
		$institute=mysql_real_escape_string($_POST['institute']);
		$department=mysql_real_escape_string($_POST['department']);
		$year_from=mysql_real_escape_string($_POST['assoc_fromyear']);
		$year_to=mysql_real_escape_string($_POST['assoc_toyear']);
		/* SQL */
		$query = "SELECT * FROM members WHERE `email`='$email'";
		$result = mysql_query($query, $con);	
		$num_rows = mysql_num_rows($result);
		if($num_rows){
			$query = "UPDATE members SET category='$category', catDetails='$cat_details', catTypeYear='$cat_type', gender='$gender', age='$age', institute='$institute', department='$department', workingFrom='$year_from', workingTo='$year_to', last_page='survey_partB1' WHERE email='$email'";	
			$result = mysql_query($query, $con);		
			if($result){
		    echo 'Form submitted successfully';
			}
			else{
				echo "Some error occured. Please fill the form again";	
			}
		}
		else{
			echo "Some error occured while processing";	
		}
}
?>
