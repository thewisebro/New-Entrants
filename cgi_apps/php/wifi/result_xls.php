<?php
include("conn.php");
function fwrite_stream($fp, $string) {
    for ($written = 0; $written < strlen($string); $written += $fwrite) {
            $fwrite = fwrite($fp, substr($string, $written));
	            if (!$fwrite) {
	return $fwrite;
	       }
	   }
        return $written;
	}
$user=$_POST["user"];
$sid=$_POST["sessionid"];
$userid = $_POST["username"];
$name = $_POST['name'];
$mac1 = $_POST["mac1"];
$mac2 = $_POST["mac2"];
$mac3 = $_POST["mac3"];
$mac4 = $_POST["mac4"];
$mac5 = $_POST["mac5"];
$mac6 = $_POST["mac6"];
$mac = $mac1.'-'.$mac2.'-'.$mac3.'-'.$mac4.'-'.$mac5.'-'.$mac6;
$bhawan = $_POST["bhawan"];
/************Converting Date Format for Database Purpose**************/
$init_date= substr($_POST["init_date"],-4).substr($_POST["init_date"],3,-5).substr($_POST["init_date"],0,2);
$final_date= substr($_POST["final_date"],-4).substr($_POST["final_date"],3,-5).substr($_POST["final_date"],0,2);
require_once 'excel.php';
if($flag=="name")
{
$result = pg_query($dbcon,"SELECT * from wifimac where name ilike '%$name%' and bhawan = '$bhawan'");
}
if($flag=="username")
{
$result = pg_query($dbcon,"SELECT * from wifimac where username='$userid'");
}
if($flag=="mac")
{
$result = pg_query($dbcon,"SELECT * from wifimac where mac='$mac'");
}
if($flag=="bhawan")
{
$result = pg_query($dbcon,"SELECT * from wifimac where bhawan='$bhawan'");
}
if($flag=="date")
{
$result = pg_query($dbcon,"SELECT * from wifimac where bhawan='$bhawan' and registered_date between '$init_date' and '$final_date'");
}
if (!$result) {
    echo "No result found.\n";
        exit;
}

$row=pg_fetch_all($result);
$count = count ($row);
  $arr = pg_fetch_all($result);
          $count = count ($arr);

?>
<div align="center">
For <? echo $bhawan ?> Bhawan, from <? echo $_POST["init_date"] ?> to <? echo $_POST["final_date"] ?>
</div><br><br>
          <table border="1">
	            <tr>
	                <td>Username </td><td>Password </td><td>Mac Address </td><td>Name </td><td>Enrollment No </td><td>Mobile </td><td>Room No </td><td>Bhawan</td><td>Registered Date </td>
		     
	             </tr>
	  <? 
	      	for ($i=0; $i<$count; $i++){
		$date = $arr[$i]['registered_date'];
		$date = substr($date,-2).'/'.substr($date,-4,-2).'/'.substr($date,0,4);
	  ?>
	  <tr>
	                <td><a href="editdetails.php?user=<? echo $user; ?>&sessionid=<? echo $sid; ?>&username=<? echo $arr[$i]['username'] ?>"><? echo $arr[$i]['username'] ?></a></td><td><?echo $arr[$i]['password']?> </td><td><? echo $arr[$i]['mac']?> </td><td><? echo $arr[$i]['name']?> </td><td><? echo $arr[$i]['enrol']?> </td><td><? echo $arr[$i]['mobile']?> </td><td><? echo $arr[$i]['roomno']?> </td><td><? echo $arr[$i]['bhawan']?> </td><td><? echo $date ?></td>
	          </tr>
<?
}

?>
</table>		  
<?
$fp = fopen("xlsfile://excel/result.xls", "wb");
if (!is_resource($fp))
{
    die( "");
}
fwrite($fp, serialize($arr));
fclose($fp);
pg_close($dbcon);
pg_close($regol);
header ("Content-Type: application/x-msexcel");
header ("Content-Disposition: attachment; filename=\"result.xls\"" );
readfile("xlsfile://excel/result.xls");
exit;
?>

