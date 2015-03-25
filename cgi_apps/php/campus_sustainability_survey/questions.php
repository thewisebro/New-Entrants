<?php
	require_once('common.php');
	require_once('constants.php');
	$count=0;
	$countgroup=4;
	foreach($partB_questions as $section=>$questions){
		$countgroup++;
		foreach($questions as $question){
			$count++;
			$number="C_".$count;
			$query="INSERT INTO questions (`question`, `number`) VALUES ('$question','$number')";
			echo $query;
			mysql_query($query,$con) or die("Error in connection. Please try again.");
		}	
	}
	
	
/*	for($i=1;$i<23;$i++){
		$var='partE_'.$i;
		$query="ALTER TABLE survey ADD $var varchar(30)";
		echo "$query";
		mysql_query($query,$con) or die('Error in query');
	}*/
?>
