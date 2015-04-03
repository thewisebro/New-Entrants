<?php
session_start();
if(!isset($_SESSION["student"]))
{	
	echo $_SESSION["student"];
	//header("Location: logout.php");
}
include('connection.php');
include('StudentLoggedIn.php');

/************                   *******************/

// session_start();
$username=$_SESSION["student"];
if($Photo)
{
if ($_FILES["Photo"]["error"] > 0)
  {
  echo "Error: " . $_FILES["Photo"]["error"] . "<br />";
  }

else
{
$filename=$_FILES['Photo']['name'];
$filelocation=$_FILES['Photo']['tmp_name'];
$filesize_byte=$_FILES['Photo']['size'];
$filesize=$filesize_byte/1024;
$ext=pathinfo($_FILES['Photo']['name']);
$fileext=$ext['extension'];
//echo "<script language='javascript'>alert('File size is $filesize kb.')</script>";
$filetype=$_FILES['Photo']['type'];
//echo "<script language='javascript'>alert('File type is $filetype.')</script>";
$uploaddir="uploads/".$username.".".$fileext;
//echo "<script type=text/javascript>alert('$fileext')</script>";
if($filesize>=100.00||($filetype!='image/jpeg' && $filetype!='image/gif' && $filetype!='image/png'))
{
echo "<script language='javascript'>alert('Can not submit. Either too big file or not a valid photo. File must be in jpeg, gif or png format less than 100 KB in size.')</script>";
}
else
{
move_uploaded_file($filelocation,$uploaddir);
$query=pg_query($dbcon,"UPDATE student_data SET photosrc='$uploaddir' where username='$username'");
}
}
}
else
{

//echo "<script language='javascript'>alert('No photo chosen.')</script>";

}

/*************************functions**************************/
require('common.php');

/***********************************************************/
if(verify_login($dbcon,$_SESSION["student"],"student")==2)
{
	include("disconnection.php");
	
	if($_SESSION['studentdata'])
	{
?>
		<script language='javascript'>
		if (document.location.hash=='') {
			document.location+='#StudentProfile';
			updateInfo('StudentProfile',1);
		}
		</script>
		 
<?	
	}
	else
	{
?>
		<script language='javascript'>
                if (document.location.hash=='') {
	                document.location+='#StudentBasicForm';
	                updateInfo('StudentBasicForm',1);
	        }
	        </script>
<?
	}
}	

?>
