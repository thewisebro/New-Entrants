<?php
	require_once('common.php');
	require_once('constants.php');
	$count=0;
	foreach($partC_questions as $section=>$questions){
		foreach($questions as $question){
			$count++;
			$number="partC_".$count;
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
