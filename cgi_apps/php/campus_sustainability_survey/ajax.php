<?php
	require('common.php');
  if(true){
		$count=0;
		$email=mysql_real_escape_string($_SESSION['email']);
		$query="SELECT * FROM members WHERE `email`='$email'";
    $result=mysql_query($query, $con);
    $result=mysql_fetch_assoc($result);
    $id=$result['id'];
    foreach($_POST as $key=>$value){
			$key=mysql_real_escape_string($key);
			$value=mysql_real_escape_string($value);
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
    echo 'Query Successful';
	}
?>
