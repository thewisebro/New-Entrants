<?php
include('conn.php');
$dbRj=pg_connect("host=192.168.121.5 dbname=regolj user=regolj password=@@l!zwell");
$query = "select enrol, username from wifimac";
$result = pg_query($dbcon, $query);


while($row = pg_fetch_row($result)) {

echo "$row[0] $row[1]";

$query_reg = "select enrollment_no from person_extended where person_id='$row[1]'";
$result_reg = pg_query($dbRj, $query_reg);
// if (!$result_reg) {
// echo " wrong";
// }
// else
// {
// echo " right";
// }
while($row_reg = pg_fetch_row($result_reg)) {
echo " $row_reg[0] ";
$query_update = "update wifimac set enrol = '$row_reg[0]' where username='$row[1]'";
echo $query_update;
pg_query($dbcon, $query_update);
}
echo "<br />";
}
?>