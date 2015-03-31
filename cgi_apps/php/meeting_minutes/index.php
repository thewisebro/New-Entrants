
<style type="text/css">
a{
text-decoration:none;
color:#7ea500;
}
</style>
<?php

function getCategoryUploads($category,$list_title,$dbcon)
{
	echo "<a name='$category'></a>";
	$query="SELECT * from meeting_minutes where category='$category' order by title";
	$res=pg_query($dbcon,$query);
	echo "<div style='width:100%'>";
	echo "<div style=''><b>$list_title</b></div><div style='float:right'> <a href='#top'>Top</a><br/>";
	echo "</div>";
	echo "<div style='width:100%'>";
	if(pg_num_rows($res)==0)
	{
		echo "No minutes have been uploaded till now<br>";
	}
	else 
	{
		echo "<ul>";	
		while($row=pg_fetch_array($res))
		{
			echo "<li><a href=\"upload/$category/".$row['filename']."\" target=\"_BLANK\" >".$row['title']."</a></li>&nbsp;";
		}
		echo "</ul>";
	}
	echo "</div>";

}
?>
<div width="100%" style="font-size:20px;font-family:verdana;text-align:center">
<b>MINUTES OF MEETINGS</b>
</div>
<hr/>
<div name="top" width="100%" style="font-family:verdana;text-decoration:none;text-align:center">
<a href="#bog">Board of Governors</a> | 
<a href="#finance">Finance Committee</a> | 
<a href="#building">Buildings & Works</a> | 
<a href="#senate">Senate</a> 
<a href="login.php" style="float:right;padding-right:5px;">Login</a>
</div>
<div width="100%" style="font-family:verdana;text-decoration:none">
<?php
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
pg_close($dbcon);
?>
</div>

