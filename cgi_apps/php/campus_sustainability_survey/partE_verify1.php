<?php
	if(isset($_POST['partE_submit'])){
    if($_SESSION['highpage']=='survey_partE1.php'){
      $_SESSION['highpage']='survey_partE2.php';
    }
 	header('location:survey_partE2.php');
	}
  else{
     //echo $_SESSION['current_page']."  ".$_SESSION['highpage']."<br/>";
      $highpage=$_SESSION['highpage'];
    if($highpage=='index.php' or $highpage=='register.php' or $highpage=='survey_partB1.php' or $highpage=='survey_partB2.php' or $highpage=='survey_partC1.php' or $highpage=='survey_partC2.php' or $highpage=='survey_partD1.php' or $highpage=='survey_partD2.php' or $highpage=='survey_partD3.php'){
      header('location:'.$_SESSION['current_page']);
    }
    else{
   		$id=$_SESSION['id'];
      $query = "UPDATE members SET last_page='survey_partE1' WHERE id=$id";
	  	mysql_query($query, $con) or die("Error in connection. Please try again.");
      $_SESSION['current_page']='survey_partE1.php';
    }  
  }

?>
