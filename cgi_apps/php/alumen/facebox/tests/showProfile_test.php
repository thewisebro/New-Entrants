<?php
 session_start();
$username=$_SESSION["username"];
if ($_FILES["Photo"]["error"] > 0)
  {
  echo "Error: " . $_FILES["Photo"]["error"] . "<br />";
  }

else
{
$filename=$_FILES['Photo']['name'];
$filelocation=$_FILES['Photo']['tmp_name'];
$filesize=$_FILES['Photo']['size'];
$uploaddir="uploads/".$username.".jpeg";
echo $uploaddir;
if(move_uploaded_file($filelocation,$uploaddir))
{
echo "<img src='$uploaddir' />";}
}
?>
