<?php
function getConnection()
{
	$db_pass="sc!ence";
	$db_user="scienceday";
	$db_name="scienceday";
	$db_host="192.168.121.9";
	$db_port="5432";

	$dbconn=pg_connect("host=$db_host dbname=$db_name user=$db_user password=$db_pass") or die("Could not connect to database.");
	return $dbconn;
}
?>
