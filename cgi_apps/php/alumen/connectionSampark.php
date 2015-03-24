<?php
$link=mssql_connect('192.168.124.202,2300','sa','daa08');
mssql_select_db("SAMPARK",$link) or die("database error");
$row2=mssql_query("select * from aspnet_Membership",$link);
$q=0;
while($row=mssql_fetch_row($row2)){
	echo $q;
	$q++;
}
?>
