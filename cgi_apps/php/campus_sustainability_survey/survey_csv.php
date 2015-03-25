<?php
  require('common.php') ;
  $FileHandle=fopen('csvdata/survey_answers.csv' ,'w') or die("Can't open the file");
  fclose($FileHandle);
  $fp = fopen('csvdata/survey_answers.csv','w');
  $qry='SHOW COLUMNS FROM survey';
  $rlt=mysql_query($qry, $con);
  $columns = array();
  while($row=mysql_fetch_array($rlt)){
    array_push($columns, $row[0]);
  }
  fputcsv($fp, $columns);
  fputcsv($fp,'\n');
  $query='SELECT * FROM survey';
  $result=mysql_query($query, $con) or die(mysql_error());  
  while($fields=mysql_fetch_assoc($result)){
    fputcsv($fp, $fields);
  }
  fclose($fp);
  header('Content-Type: application/csv');
  header('Content-Disposition: attachment; filename=survey_answers.csv');
  header('Pragma: no-cache');
  readfile('csvdata/survey_answers.csv');
  unlink('csvdata/survey_answers.csv');
?>

