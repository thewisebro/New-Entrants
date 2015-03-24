<?php
	if(isset($_POST['partB_submit'])){
		$count=0;
		$email=mysql_real_escape_string($_SESSION['email']);
		$query="SELECT * FROM members WHERE `email`='$email'";
    $result=mysql_query($query, $con) or die("Error in connection. Please try again.");
    $result=mysql_fetch_assoc($result);
    $id=$result['id'];
    foreach($_POST as $key=>$value){
			if($key=='partB_submit'){
				continue;	
			}
			$key=mysql_real_escape_string($key);
			$value=mysql_real_escape_string($value);
			$count++;
      $query="SELECT * FROM survey WHERE person_id=$id and question='$key'";
      $result=mysql_query($query, $con) or die(mysql_error());
      $num_rows=mysql_num_rows($result);
      if($num_rows){
        $query="UPDATE survey SET answer='$value' WHERE person_id=$id and question='$key'";
      }
      else{
        $query="INSERT INTO survey (person_id,question,answer) VALUES ($id,'$key','$value')";
      }
      $result=mysql_query($query, $con) or die(mysql_error()); 
    }
   if($_SESSION['highpage']=='survey_partB1.php'){
      $_SESSION['highpage']='survey_partB2.php';
    }
   	header('location:survey_partB2.php');
	}
  else{
    echo $_SESSION['current_page']."  ".$_SESSION['highpage']."<br/>";
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
