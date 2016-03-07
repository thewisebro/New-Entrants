<?php
	require_once('common.php');
	require_once('constants.php');
	/*for($i=139;$i<=252;$i++){
		$query="SELECT * FROM questions WHERE id='$i'";
		$result=mysql_query($query, $con) or die("Error in connection. Please try again.");
		//echo $result;
		$result=mysql_fetch_assoc($result);
		$number=$result['number'];
		$str=explode('_',$number);
		//echo $str[0];
		//echo $str[1];
		$count=$str[1]-1;
		$section = $sections_D[$count];
		//echo $section;	
		$query="UPDATE questions SET section='$section' WHERE id='$i'";
		$result=mysql_query($query, $con) or die("Error in connection. Please try again.");
		echo $query;
	}*/

	
  //INSERT QUESTIONS OF PART D
  /*$count=0;
	$count_group=2;
	foreach($partE_questions_2 as $section=>$questions){
		$count_group++;
		$count=0;
		foreach($questions as $question){
			$count++;
			$number="E_".$count_group."_".$count;
			$section=$sections_E[$count_group-1];
			$query="INSERT INTO questionaire (`question`, `number`, `section`) VALUES ('$question','$number','$section')";
			mysql_query($query,$con) or die(mysql_error());
			echo $query;
			$number="D_".$count_group."_".$count."_WASTE";
			$section=$sections_D[$count_group-1];
			$query="INSERT INTO questionaire (`question`, `number`, `section`) VALUES ('$question','$number','$section')";
			mysql_query($query,$con) or die("Error in connection. Please try again.");
			echo $query;
			$number="D_".$count_group."_".$count."_WATER";
			$section=$sections_D[$count_group-1];
			$query="INSERT INTO questionaire (`question`, `number`, `section`) VALUES ('$question','$number','$section')";
			mysql_query($query,$con) or die("Error in connection. Please try again.");
			echo $query;
    }	
	}*/
  

	/*$query="SELECT * FROM questions WHERE id>=2";
	$result=mysql_query($query, $con) or die("Error in connection. Please try again.");
	while($row = mysql_fetch_assoc($result)){
		$number=$row['number'];
		$str=explode('_',$number);
		if($str[0]=='D'){
			$number=$number."_ENERGY";
			$query="ALTER TABLE survey ADD $number varchar(30)";	
			mysql_query($query, $con) or die("Error in connection. Please try again.");	
			echo "$query";
			$number=$row['number'];
			$number=$number."_WASTE";
			$query="ALTER TABLE survey ADD $number varchar(30)";	
			mysql_query($query, $con) or die("Error in connection. Please try again.");
			echo "$query";
			$number=$row['number'];
			$number=$number."_WATER";
			$query="ALTER TABLE survey ADD $number varchar(30)";	
			echo "$query";
			mysql_query($query, $con) or die("Error in connection. Please try again.");
		}
		else{
			$query="ALTER TABLE survey ADD $number varchar(30)";	
			mysql_query($query, $con) or die("Error in connection. Please try again.");
		}
	}*/
	

		/*for($i=1;$i<23;$i++){
		$var='partE_'.$i;
		$query="ALTER TABLE survey ADD $var varchar(30)";
		echo "$query";
		mysql_query($query,$con) or die('Error in query');*/
	

	/*$query = "SELECT * FROM questions WHERE id>0 and id<10";
	$rlt = mysql_query($query, $con) or die("Error in connection. Please try again.");
	$count=9;
	while($row = mysql_fetch_assoc($rlt)){
		$str=explode('_',$row['number']);
		echo $str[1];
		echo "\n";
	}*/
?>
