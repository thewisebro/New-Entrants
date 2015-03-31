<?php
	if(isset($_POST['partB_submit'])){
    if($_SESSION['highpage']=='survey_partB1.php'){
      $_SESSION['highpage']='survey_partB2.php';
    }
   	header('location:survey_partB2.php');
	}
  else{
    //echo $_SESSION['current_page']."  ".$_SESSION['highpage']."<br/>";
    $highpage=$_SESSION['highpage'];
    if($highpage=='index.php' or $highpage=='register.php'){
      header('location:'.$_SESSION['current_page']);
    }
    else{
      $id=$_SESSION['id'];
      $query = "UPDATE members SET last_page='survey_partB1' WHERE id=$id";
	  	mysql_query($query, $con) or die("Error in connection. Please try again.");
      $_SESSION['current_page']='survey_partB1.php';
    }  
  }
?>
