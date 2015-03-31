<html>
	<head>
		<title>Registered Students</title>
	</head>
<?
/**********************************************************************/
/*** To see the registered students details by various search and export search result in Excel formal********/
/******By CS Vikram*********************************/
/**********************************************************************/

?>
<body>
<form name="WifiMain" action="admin.php" method="post">
<table >
<tr>
	<td><input type="radio" name='flag' value='name'></input>
	Search by Name
	<td><input type="text" name="name">
</tr>
<tr>
	<td><input type="radio" name='flag' value='username'></input>
	Search by Username 
	<td><input type="text" name="username">
</tr>
<tr>
	<td><input type="radio" name='flag' value='date'></input>
	Search by Date
<tr>
 <tr>
   <td>Starting Date </td>
   <td>
	Date: <input type="text" name="init_date" value="dd/mm/yyyy" size="15" maxlength="10"> 
	<input type="button" name="cmdCal" value="Launch Calendar" onClick='javascript:window.open("calendar.php?form=WifiMain&field=init_date","","top=50,left=400,width=175,height=140,menubar=no,toolbar=no,scrollbars=no,resizable=no,status=no"); return false;'>
  </td>
</tr>
<tr>
   <td>Final Date </td>
   <td>
	Date: <input type="text" name="final_date" value="dd/mm/yyyy" size="15" maxlength="10"> 
	<input type="button" name="cmdCal" value="Launch Calendar" onClick='javascript:window.open("calendar.php?form=WifiMain&field=final_date","","top=50,left=400,width=175,height=140,menubar=no,toolbar=no,scrollbars=no,resizable=no,status=no"); return false;'>
  </td>
</tr>
<tr>
	<td><input type="radio" name='flag' value='Mac'></input>
	Search by Mac
<tr>
</tr>
<tr>
   <td>MAC/Physical Address</td>
   <td><input type="text" name="mac1" size="2"/>
        <input type="text" name="mac2" size="2" />
	<input type="text" name="mac3" size="2"/>
	<input type="text" name="mac4" size="2"/>
       <input type="text" name="mac5" size="2"/>
        <input type="text" name="mac6" size="2"/></td>
 </tr>
<tr>
	<td><input type="radio" name='flag' value='Bhawan'></input>
	Search by Bhawan 
     <td>
           <select name="bhawan">
           <option value="Kasturba">Kasturba</option>
           <option value="Sarojini">Sarojini</option>
         </select>
     </td>
 </tr>
 <tr><td><input type="submit" name="submit"  value="submit"></td></tr>
 </table>


<?php
//error_reporting(E_ALL);
include("conn.php");
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
$init_date= substr($_POST["init_date"],-4).substr($_POST["init_date"],3,-5).substr($_POST["init_date"],0,2);;
$final_date= substr($_POST["final_date"],-4).substr($_POST["final_date"],3,-5).substr($_POST["final_date"],0,2);;

require_once 'excel.php';

if($flag=="name")
{
$result = pg_query($dbcon,"SELECT * from wifimac where name ilike '%$name%'");
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
$result = pg_query($dbcon,"SELECT * from wifimac where registered_date between '$init_date' and '$final_date'");
}
if (!$result) {
    echo "No result found.\n";
        exit;
}
//$row=pg_fetch_all($result);
$count = count ($row);
  $arr = pg_fetch_all($result);
          $count = count ($arr);

?>
          <table>
	            <tr>
	                <td>name </td><td>enrol </td><td>email </td><td>mac </td><td>roomno </td><td>bhawan </td><td>mobile </td><td>username </td><td>registered_date </td>
	             </tr>
	  <?
	        for ($i=0; $i<$count; $i++){
	  ?>
	          <tr>
	                <td><? echo $arr[$i]['name'] ?></td><td><?echo $arr[$i]['enrol']?> </td><td><? echo $arr[$i]['email']?> </td><td><? echo $arr[$i]['mac']?> </td><td><? echo $arr[$i]['roomno']?> </td><td><? echo $arr[$i]['bhawan']?> </td><td><? echo $arr[$i]['mobile']?> </td><td><? echo $arr[$i]['username']?> </td><td><? echo $arr[$i]['registered_date']?> </td>
	          </tr>
	   <?
	                      echo $arr[$i]['enrol'].'-'.$arr[$i]['email'].'-'.$arr[$i]['mac'].'-'.$arr[$i]['roomno'].'-'.$arr[$i]['bhawan'].'-'.$arr[$i]['mobile'].'-'.$arr[$i]['username'].'-'.$arr[$i]['registered_date'];
		}																		                       ?>																					          </table>
																							<?

$fp = fopen("xlsfile://excel/result.xls", "wb");
/*
if (!is_resource($fp))
{
    die( "Cannot open $export_file");
    echo 'cannot open excelfile to write';
}
	fwrite($fp, serialize($row));
	fclose($fp);

pg_close($dbcon);


                   header ("Content-Type: application/x-msexcel");
	           header ("Content-Disposition: attachment; filename=\"result.xls\"" );
	           readfile("xlsfile://excel/result.xls");
	           exit;
*/
?>


</body>

</html>

