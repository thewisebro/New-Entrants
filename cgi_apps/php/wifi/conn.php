<?
ini_set("display_errors", "off");
$dbcon=mysql_connect("192.168.121.9","wifi","wifi");
mysql_select_db("channeli",$dbcon);
if(!$dbcon)
  echo "Not Connected";
?>
