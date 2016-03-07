<?php
	$email=$_SESSION['email'];
	if(isset($_POST['details_submit'])){
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
		$result = mysql_query($query, $con) or die("Error in connection. Please try again.");	
		$num_rows = mysql_num_rows($result);
		if($num_rows){
			$query = "UPDATE members SET category='$category', catDetails='$cat_details', catTypeYear='$cat_type', gender='$gender', age='$age', institute='$institute', department='$department', workingFrom='$year_from', workingTo='$year_to', last_page='survey_partB1' WHERE email='$email'";	
			$result = mysql_query($query, $con) or die("Error in connection. Please try again.");		
			if($result){
	      if($_SESSION['highpage']=='register.php'){
           $_SESSION['highpage']='survey_partB1.php';
        }
 		  	$_SESSION['register']=0;
        header('location:survey_partB1.php');
			}
			else{
				die("Some error occured. Please fill the form again");	
			}
		}
		else{
			die("Some error occured while processing");	
		}
}
  else{
    $id=$_SESSION['id'];
    //echo "current page=".$_SESSION['current_page']."  highpage=".$_SESSION['highpage']."<br/>";
    if(isset($_SESSION['register']) and $_SESSION['register']==1){
        $_SESSION['current_page']='register.php';
    
    }
    else{
      header('location:'.$_SESSION['current_page']);
    }
  }
?>
