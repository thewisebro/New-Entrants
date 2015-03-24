<?php
  require('common.php');
  if(isset($_POST['ajax_submit'])){
 		$email=mysql_real_escape_string($_SESSION['email']);
		$query="SELECT * FROM members WHERE `email`='$email'";
    $result=mysql_query($query, $con);
    $result=mysql_fetch_assoc($result);
    $id=$result['id'];
    $key=mysql_real_escape_string($_POST['name']);
    $value=mysql_real_escape_string($_POST['value']);
    $count++;
    $query="SELECT * FROM survey WHERE person_id=$id and question='$key'";
    $result=mysql_query($query, $con);
    $num_rows=mysql_num_rows($result);
    if($num_rows){
      $query="UPDATE survey SET answer='$value' WHERE person_id=$id and question='$key'";
    }
    else{
      $query="INSERT INTO survey (person_id,question,answer) VALUES ($id,'$key','$value')";
    }
    $result=mysql_query($query, $con); 
  }
?>
