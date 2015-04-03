<html>
<head>
<!--<style text="css/text">
body {
font-family:Trebuchet MS, Verdana;
}
a {text-decoration:none;}
table,tr,td {border:solid 1px #000;
font-family:Trebuchet MS, Verdana;
font-size:13px;
}
</style>-->
</head>
<body>
<?php
//error_reporting(0);
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
$userid = $_POST["username"];
$name = $_POST['name'];
$mac1 = $_POST["mac1"];
$mac2 = $_POST["mac2"];
$mac3 = $_POST["mac3"];
$mac4 = $_POST["mac4"];
$mac5 = $_POST["mac5"];
$mac6 = $_POST["mac6"];
$submit = $_POST["submit"];
$flag = $_POST["flag"];
$mac = $mac1.'-'.$mac2.'-'.$mac3.'-'.$mac4.'-'.$mac5.'-'.$mac6;
//***********************************************added by mohit
$no_of_bhawans_selected=0;
foreach($_POST['bhawan'] as $value)
{
$no_of_bhawans_selected+=1;
$bhawan_query.="'$value' or bhawan=";	
$bhawans1.=$value.",";
}
$bhawanquery= substr($bhawan_query,0 ,-11);
echo $bhawanquery;
$bhawans= substr($bhawans1,0,-1);
//**********************************************added by mohit
//echo $no_of_bhawans_selected." ".$bhawanquery;

/************Converting Date Format for Database Purpose**************/
$init_date= substr($_POST["init_date"],-4).substr($_POST["init_date"],3,-5).substr($_POST["init_date"],0,2);
$final_date= substr($_POST["final_date"],-4).substr($_POST["final_date"],3,-5).substr($_POST["final_date"],0,2);
require_once 'excel.php';
echo $init_date." ".$final_date;
echo $flag;
if($flag=="name")
{
$result = mysql_query("SELECT * from wifimac where name like '%$name%' and (bhawan = $bhawanquery) order by bhawan",$dbcon);
}
if($flag=="username")
{
$result = mysql_query("SELECT * from wifimac where username='$userid'",$dbcon);
}
if($flag=="mac")
{
$result = mysql_query("SELECT * from wifimac where mac='$mac'",$dbcon);
}
if($flag=="bhawan")
{
$result = mysql_query("SELECT * from wifimac where bhawan=$bhawanquery order by bhawan",$dbcon);
}
if($flag=="date")
{
$result = mysql_query("SELECT * from wifimac where (bhawan=$bhawanquery) and registered_date between '$init_date' and '$final_date' order by bhawan",$dbcon);
}
if (!$result) {
    echo "No result found.\n";
    exit;
}
/*
function cleanData(&$str) { $str = str_replace(";",",",$str); $str = preg_replace("/\t/", "\\t", $str); $str = preg_replace("/\r?\n/", "\\n", $str); if(strstr($str, '"')) $str = '"' . str_replace('"', '""', $str) . '"'; } # file name for download 
$filename = "result.xls"; 
header("Content-Disposition: attachment; filename=\"$filename\""); 
header("Content-Type: application/vnd.ms-excel"); 

$flag=false;

while(false !== ($row = mysql_fetch_assoc($result))) {  if(!$flag) {
if($row=='')
{
        echo "\tmohit\n";
}	
# display field/column names as first row 
echo "\t\t$headingofexcel\t\t\n";
echo implode("\t", array_keys($row)) . "\n"; $flag = true; } array_walk($row, 'cleanData'); echo implode("\t", array_values($row)) . "\n"; }
*/
/*-----change for mysql 
//$row=mysql_fetch_all($result);
//$count = count ($row);
//  $arr = mysql_fetch_all($result);
//          $count = count ($arr);
*/
?>
<div align="center">
For <? echo $bhawans ?> Bhawans  from <? echo $_POST["init_date"] ?> to <? echo $_POST["final_date"] ?>
</div><br><br>
          <table cellspacing="0" cellpadding="1">
	            <tr>
	                <td>AccountName </td><td>userPrincipalName </td><td>givenName</td><td>sn</td><td>description</td><td>password </td><td>physicalDeliveryOfficeName</td><td>telephoneNumber</td><td>streetAddress</td>
		     
	             </tr>
	  <?
	  if (file_exists("excel/result.xls")) { unlink("excel/result.xls"); }
	  /*$fp = fopen("./excel/result.xls", "wb");

	   for ($i=0; $i<$count; $i++)
	   {
	  	$line=$arr[$i]['username']."\t".$arr[$i]['username'].'@'. strtolower($arr[$i]['bhawan']).'wifi.com'."\t".$arr[$i]['name']."\t".$arr[$i]['enrol']."\t".$arr[$i]['password']."\t".$arr[$i]['mac']."\t".$arr[$i]['mobile']."\t".$arr[$i]['roomno'].", ".$arr[$i]['bhawan']." Bhawan \t TRUE \n";
		echo $line;
	fwrite($fp, $line);*/

	
	  /* 
	  ?>
	  <tr>
	                <td><a href="editdetails.php?user=<? echo $user; ?>&sessionid=<? echo $sid; ?>&username=<? echo $arr[$i]['username'] ?>"><? echo $arr[$i]['username'] ?></a></td><td><? echo $arr[$i]['username'].'@'. strtolower($arr[$i]['bhawan']).'wifi.com'; ?></td><td><? echo $arr[$i]['name']; ?> </td><td></td><td><? echo $arr[$i]['enrol'];?> </td><td><? echo $arr[$i]['password'];?> </td><td><? echo $arr[$i]['mac'];?> </td><td><? echo $arr[$i]['mobile'];?> </td><td><? echo $arr[$i]['roomno'].','.$arr[$i]['bhawan'].' Bhawan'; ?></td><td>TRUE</td>
	          </tr>
<?
*/


//}



if (file_exists("excel/result.csv")) { unlink("excel/result.csv"); }

$fp=fopen("excel/result.csv","w");
var_dump($fp);
$line=array('sAMAccountName','userPrincipalName','givenName','sn','description','password','physicalDeliveryOfficeName','telephoneNumber','streetAddress',);
fputcsv($fp,$line);

while($row=mysql_fetch_array($result))
{
  //var_dump($row);
	$line=array($row['username'],$row['username'].'@'. strtolower($row['bhawan']).'wifi.com',$row['name'],'',$row['enrol'],$row['password'],$row['mac'],$row['mobile'],$row['roomno'].", ".$row['bhawan']." Bhawan");
	
	fputcsv($fp,$line);
}

/*foreach($arr as $line)
{	
fputcsv($fp,$line);
}
*/
fclose($fp);

mysql_close($dbcon);


echo "<a href=\"download.php\">Click to Download</a>"

?>
</table>		  
<?
//$fp = fopen("xlsfile://excel/result.xls", "wb");

/*
$fp = fopen("./excel/result.xls", "wb");
if (!is_resource($fp))
{
if ($submit!="")    die("");
}
fwrite($fp, serialize($arr));
fclose($fp);

mysql_close($dbcon);
mysql_close($regol);



header ('Content-Type: application/vnd.ms-excel');
header ('Content-Disposition: attachment; filename="result.xls"' );
readfile("xlsfile://excel/result.xls");
//readfile("./excel/result.xls");
//readfile("./excel/result.xls");
exit;
*/
//header('Location: ./excel/result.xls');


/*header('Content-Description: File Transfer');
header('Content-Type: application/x-msexcel');
header('Content-Disposition: attachment; filename="result.csv"');
header('Content-Transfer-Encoding: binary');
header('Expires: 0');
header('Cache-Control: must-revalidate, post-check=0, pre-check=0');
header('Pragma: no-cache');*/
//header('Content-Length: ' . filesize("./excel/result.xls"));
//ob_clean();
//flush();
//readfile("./excel/result.xls");
 

/*echo "
<script type='text/javascript'>
window.location='excel/result.csv';
</script>
";*/
//unlink("excel/result.xls");
exit;
?>

