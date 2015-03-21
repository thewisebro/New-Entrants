<?php
//include("../includes/get-username.php");
//include("../includes/require-login.php");
include("auth.php");
echo '<form action="upload.php">';
include("connection.php");
	
$dbconn=getConnection();
$number = intval($_POST['number']);
echo $number;
for($i = 1;$i<=$number;$i++)
{
/*if ((($_FILES["ufile$i"]["type"] == "image/gif")
|| ($_FILES["ufile$i"]["type"] == "image/jpeg")
|| ($_FILES["ufile$i"]["type"] == "image/jpg")))

{*/
 if ($_FILES["ufile$i"]["error"] > 0)
   {
   echo "Error : ".$_FILES["ufile$i"]['error']."<br />";
   }
 else
   {
   echo "<br />Upload : ".$_FILES["ufile$i"]['name']."<br />";

   echo "Temp file : ".$_FILES["ufile$i"]['tmp_name']."<br />";
   
   if (file_exists("upload/".$_FILES["ufile$i"]['name']))
   	{
	echo $_FILES["ufile$i"]['name']." already exists";
	}
   else
   	{
	$query2="Select id from scienceday_photos;";
	$result2=pg_query($dbconn,$query2);
	$rows=pg_num_rows($result2);
//	echo $rows;

	move_uploaded_file($_FILES["ufile$i"]['tmp_name'],"upload/".$_FILES["ufile$i"]['name']);
?>
	<img src="<?php echo "upload/".$_FILES["ufile$i"]['name'] ?>"><p>
<?php	
	echo "Stored in folder in upload/".$_FILES["ufile$i"]['name']."<br />";
	echo "Stored in database as image".$rows.".jpg";
	
   
$query="Insert into scienceday_photos (old_location,new_location) VALUES ('upload/".$_FILES["ufile$i"]['name']."','upload/image".$rows.".jpg' );";


$result=pg_query($dbconn,$query);
 if (!$result){
 echo "An error occured.\n";
 exit;
}  } 
   }
/*}

else
{
  echo "Invalid file. File type should be JPEG/JPG/GIF type.";
 }*/
}
?>
<input type="submit" value="Go back to File Upload">
</form>
<form action="index.php">
<Input Type="submit" Value="Go to the Picture View">
</form>
