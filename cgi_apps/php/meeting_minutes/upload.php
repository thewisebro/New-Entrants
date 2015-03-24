<?php
session_start();
if( !isset($_SESSION["username"]) || !isset($_SESSION["password"]) || $_SESSION["username"]!="ajay" || $_SESSION["password"]!="m!nutes")
{
	header("location:logout.php");
}
if($_GET["err"]==1)
	echo "<br/>File upload error<br/>";
?>
<a href="logout.php">Logout</a><br/><br/>
<form action="upload_file.php" method="POST" enctype="multipart/form-data" >
Title:<input type="text" name="title"/><br/>
Category:<select name="category">
	<option value="bog">Board of Governors</option>
	<option value="finance">Finance Committee</option>
	<option value="building">Building and Works</option>
	<option value="senate">Senate</option>
	<option value="dairy">Dairy</option>
	</select><br/>
File:<input type="file" name="file"/><br/>
<input type="submit" name="submit" value="Upload"/>
</form>

<?php
	echo "<br/><br/><b><u>Minutes of meetings</u></b><br/>";
  include("connectionFile.php");
  $dbcon=getConnection("meeting_minutes","meeting_minutes");
	echo "<hr/>";
	getCategoryUploads("bog","Board of Governors",$dbcon);
	echo "<hr/>";
	getCategoryUploads("finance","Finance Committee",$dbcon);
	echo "<hr/>";
	getCategoryUploads("building","Buildings and Works",$dbcon);
	echo "<hr/>";
	getCategoryUploads("senate","Senate",$dbcon);
	echo "<hr/>";
	getCategoryUploads("dairy","Dairy",$dbcon);
	echo "<hr/>";

	pg_close($dbcon);

function getCategoryUploads($category,$list_title,$dbcon)
{
	$query="SELECT * from meeting_minutes where category='$category'";
	$res=pg_query($dbcon,$query);
	echo "<b>$list_title</b><br/>";
	if(pg_num_rows($res)==0)
	{
		echo "No minutes have been uploaded till now<br>";
	}
	else 
	{
		echo "<ul>";	
		while($row=pg_fetch_array($res))
		{
			echo "<li ><a href=\"upload/$category/".$row['filename']."\" target=\"_BLANK\">".$row['title']."</a></li>&nbsp;<a href='delete_file.php?id=".$row['meeting_id']."'>Delete</a>";
		}
		echo "</ul>";
	}

}
?>

