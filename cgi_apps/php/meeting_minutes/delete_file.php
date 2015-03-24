<?php
session_start();
if( !isset($_SESSION["username"]) || !isset($_SESSION["password"]))
{
	header("location:logout.php");
}
	$err=0;
  include("connectionFile.php");
  $dbcon=getConnection("meeting_minutes","meeting_minutes");
	$query="select filename,category from meeting_minutes where meeting_id=".$_GET["id"];
	$res=pg_query($dbcon,$query);
	while($row=pg_fetch_array($res))
	{
		$filename=$row[0];
		$category=$row[1];
	}
	if(unlink("upload/$category/".$filename))
	{
		$query="delete from meeting_minutes where meeting_id=".$_GET["id"];
    var_dump($query);
		$res=pg_query($dbcon,$query);
		if(!$res)
			$err=1;
		echo pg_last_error();
	}
	else
	$err=1;
	pg_close($dbcon);
if($_SESSION["username"]=="ajay")
  	header("location:upload.php?err=$err");
  else
  	header("location:upload_dairy.php?err=$err");


?>
