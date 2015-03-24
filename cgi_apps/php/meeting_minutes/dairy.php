
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
	$query="SELECT * from meeting_minutes where category='$category'";
	$res=pg_query($dbcon,$query);
	echo "<div style='width:100%'>";
	echo "<div style=''><b>$list_title</b></div><div style='float:right'> <a href='#top'>Top</a><br/>";
	echo "</div>";
	echo "<div style='width:100%'>";
	if(pg_num_rows($res)==0)
	{
		echo "No reports have been uploaded till now<br>";
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
<b>DAIRY REPORTS</b>
</div>
<hr/>
<div name="top" width="100%" style="font-family:verdana;text-decoration:none;text-align:center">
</div>
<div width="100%" style="font-family:verdana;text-decoration:none">
<?php
include("connectionFile.php");
$dbcon=getConnection("meeting_minutes","meeting_minutes");
getCategoryUploads("dairy","Dairy",$dbcon);
echo "<hr/>";
pg_close($dbcon);
?>
</div>

