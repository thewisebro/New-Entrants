<?php
session_start();
error_reporting(0);
ini_set("display_errors", 1);
if( !isset($_SESSION["username"]) || !isset($_SESSION["password"]))
{
  header("location:logout.php");
}

$err=0;
if ($_FILES["file"]["error"] > 0)
  {
    echo "Error: " . $_FILES["file"]["error"] . "<br />";
    $err=1;
  }
  else
  {
	  echo "Upload: " . $_FILES["file"]["name"] . "<br />";
	  $path="upload/".$_POST["category"]."/".$_FILES["file"]["name"];
	  if (file_exists($path))
          {
		 echo $_FILES["file"]["name"] . " already exists. ";
		 $err=1;
          }
          else
	  {
	        if(move_uploaded_file($_FILES["file"]["tmp_name"],$path))
		        echo "Stored in: $path";
		else
		$err=1;
    include("connectionFile.php");
    $dbcon=getConnection("meeting_minutes","meeting_minutes");
		$query="insert into meeting_minutes(filename,title,category) values('".$_FILES["file"]["name"]."','".$_POST["title"]."','".$_POST["category"]."')";
		pg_query($dbcon,$query);
		pg_close($dbcon);

	  }
  }
  if($_SESSION["username"]=="ajay")
  	header("location:upload.php?err=$err");
  else
  	header("location:upload_dairy.php?err=$err");
?>
