<?php
//error_reporting('E_ALL');
include_once("../common/functions.php");
database::connectToDatabase();
$conn_lectut=pg_connect('host=192.168.121.147 dbname=lectut user=lectut password=lectuT') or die('Could not connect');

$qlec="select faculty_id,course_id,file,topic,permission,timestamp from lectures;";

$qtut="select faculty_id,course_id,file,topic,permission,timestamp from tutorials;";

$qexam="select faculty_id,course_id,file,topic,permission,timestamp,year from exam_papers;";

$qsoln="select faculty_id,course_id,file,topic,permission,timestamp,link_type,link_id from solutions;";

$qdesign="select faculty_id,choice from design_choice;";

//truncate new tables
$return = database::executeQuery("truncate table lectut_lectures;");
$return = database::executeQuery("truncate table lectut_tutorials;");
$return = database::executeQuery("truncate table lectut_exam_papers;");
$return = database::executeQuery("truncate table lectut_solutions;");
$return = database::executeQuery("truncate table lectut_design_choice;");

$q=pg_query($conn_lectut,$qlec);
while($row=pg_fetch_row($q))
{
  $newq="insert into lectut_lectures (faculty_id,course_id,file,topic,permission,timestamp) values ('$row[0]','$row[1]','$row[2]','$row[3]',false,'$row[5]')";
  $return = database::executeQuery($newq);
}

$q=pg_query($conn_lectut,$qtut);
while($row=pg_fetch_row($q))
{
  $newq="insert into lectut_tutorials (faculty_id,course_id,file,topic,permission,timestamp) values ('$row[0]','$row[1]','$row[2]','$row[3]',false,'$row[5]')";
	$return = database::executeQuery($newq);
}

$q=pg_query($conn_lectut,$qexam);
while($row=pg_fetch_row($q))
{
  $newq="insert into lectut_exam_papers (faculty_id,course_id,file,topic,permission,timestamp,year) values ('$row[0]','$row[1]','$row[2]','$row[3]',false,'$row[5]','$row[6]')";
	$return = database::executeQuery($newq);
}

$q=pg_query($conn_lectut,$qsoln);
while($row=pg_fetch_row($q))
{
  //  $newq="insert into lectut_solutions (faculty_id,course_id,file,topic,permission,timestamp,link_type,link_id) values ('$row[0]','$row[1]','$row[2]','$row[3]',false,'$row[5]','$row[6]',$row[7])";

  $newq="insert into lectut_solutions (faculty_id,course_id,file,topic,permission,timestamp) values ('$row[0]','$row[1]','$row[2]','$row[3]',false,'$row[5]')";
	$return = database::executeQuery($newq);
}

$q=pg_query($conn_lectut,$qdesign);
while($row=pg_fetch_row($q))
{
  if($row[1]=='f')
    $choice='false';
  else
    $choice='true';
  $newq="insert into lectut_design_choice (faculty_id,choice) values('$row[0]',$choice)";
	$return = database::executeQuery($newq);
}

pg_close($conn_lectut);
database::closeDatabase();

?>
