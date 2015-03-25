<?php
include("../conn.php");
if (!$dbcon) {
    echo "An error occured.\n";
            exit;
	   } 
          $result = pg_query($dbcon, "SELECT * FROM wifimac");
            if (!$result) {
          echo "An error occured.\n";
            exit;
	                  }
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
	           
	}
					
	?>
	</table>
	<?
$fp = fopen("xlsfile://../excel/result.xls", "wb");
if (!is_resource($fp))
{
    die("Cannot open $export_file");
        echo 'cannot open excelfile to write';
	}
	        fwrite($fp, serialize($arr));
		        fclose($fp);

header ("Content-Type: application/x-msexcel");
           header ("Content-Disposition: attachment; filename=\"result.xls\"" );
           readfile("xlsfile://../excel/result.xls");
           exit;
?>

