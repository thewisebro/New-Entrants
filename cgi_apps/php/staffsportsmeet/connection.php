<?php
function getConnection()
{
	$db_pass="cms";
	$db_user="cms";
	$db_name="cms";
	$db_host="192.168.121.5";
	$db_port="5432";

	$dbconn=pg_connect("host=$db_host dbname=$db_name user=$db_user password=$db_pass") or die("Could not connect to database.");
	return $dbconn;
}
?>
