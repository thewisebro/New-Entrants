<?php 
// CONNECTION FILE FOR GETTING CONNECTION TO VARIOUS DATABASES 


function getConnection($database,$user){
	$password="";
	switch($user){
		case "meeting_minutes":
			$password="m!nutes";
			break;
		default:
			$passsword=NULL;
	}
		$dbcon=pg_connect("host=192.168.121.9 port=5432 dbname=$database user=$user password=$password"); //or die("Database Connection Failed");
	return $dbcon;
}
?>
