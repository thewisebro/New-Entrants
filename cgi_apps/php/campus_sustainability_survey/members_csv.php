<?php
  require('common.php');
  $FileHandle=fopen('csvdata/members.csv','w') or die("Can't write the file");
  fclose($FileHandle);
  $fp = fopen('csvdata/members.csv','w');
  $qry='SHOW COLUMNS FROM members';
  $rlt=mysql_query($qry, $con);
  $columns = array();
  while($row=mysql_fetch_array($rlt)){
    array_push($columns, $row[0]);
  }
  fputcsv($fp, $columns);
  $query='SELECT * FROM members';
  $result=mysql_query($query, $con) or die(mysql_error());
  while($fields=mysql_fetch_assoc($result)){
    fputcsv($fp, $fields);
  }
  fclose($fp);
  header('Content-Type: application/csv');
  header('Content-Disposition: attachment; filename=members.csv');
  header('Pragma: no-cache');
  readfile('csvdata/members.csv');
  unlink('csvdata/members.csv');
?>


