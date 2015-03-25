<?php
header('Content-Type: application/json');
require 'connection.php';
if (isset($_GET['term']))
{
  $word=$_GET['term'];
  $return_array = array();
  $query1= mysqli_query($var, "SELECT equipname FROM equip_entries WHERE equipname LIKE '%$word%' LIMIT 10" );
  while($row = mysqli_fetch_array($query1))
  {
    $return_array[] = $row['equipname'];
  }
  echo json_encode($return_array);
}
?>
