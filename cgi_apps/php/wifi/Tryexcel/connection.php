<?
//a copy of this intranet db also lies on .7 but it is old and unupdated so let the copy of intranet .5 be used for lecTut. Still facapp db of .7 is being used because Faculty Profile still uses that one.

$dbcon=pg_connect("host=192.168.121.5 dbname=intranet user=img password=@ll!zwell") or die("Could not Connect");
$regol=pg_connect("host=192.168.121.5 dbname=regolj user=regolj password=@ll!zwell") or die("Could not Connect");
?>
