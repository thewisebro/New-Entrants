<?php
require 'connection.php';
$dept = $_GET["val"];
echo "DEPARTMENT-";
echo $dept;
echo "<br>";
//echo "deptname profname<br>";
$values = mysqli_query($var, "SELECT * FROM equip_entries WHERE deptname = '$dept'");
echo "<table border='1' class='table table-striped'>
<tr>
<th>Equipment</th>
<th>Professor</th>
</tr>";
 while($row = mysqli_fetch_array($values)) 
{
  echo "<tr>";
  echo "<td>".$row['equipname']."</td>";  
  echo "<td>".$row['profname']."</td>";
  echo "</tr>";
}
echo "</table>";
?>
