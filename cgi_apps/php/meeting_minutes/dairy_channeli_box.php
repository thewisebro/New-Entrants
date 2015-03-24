
<style type="text/css">
a{
font-family:Verdana, Arial, Helvetica, sans-serif;
text-decoration:none;
font-size:12px;
color:#222;
}
a:hover
{
	text-decoration:underline;
}
</style>
<?php

function getCategoryUploads($category,$list_title,$dbcon)
{
	echo "<a name='$category'></a>";
	$query="SELECT * from meeting_minutes where category='$category'";
	$res=pg_query($dbcon,$query);
	echo "<div style='width:100%'>";
//	echo "<div style=''><b>$list_title</b></div><div style='float:right'><br/>";
	echo "</div>";
	echo "<div style='width:100%'>";
	if(pg_num_rows($res)==0)
	{
		echo "No new reports uploaded<br/>";
	}
	else
	{
		$i=1;
		while($row=pg_fetch_array($res))
		{
			echo "<a href=\"upload/$category/".$row['filename']."\" target=\"_BLANK\" >".$row['title']."</a>&nbsp;<br/><br/>";
			$i++;
			if($i>3)
				break;
		}
	}
	echo "</div>";

}
?>
<div name="top" width="100%" style="font-family:verdana;text-decoration:none;text-align:center">
</div>
<div width="100%" style="font-family:verdana;text-decoration:none">
<?php
	include("connectionFile.php");
	$dbcon=getConnection("meeting_minutes","meeting_minutes");
	getCategoryUploads("dairy","",$dbcon);
?>
<a href="dairy.php" style="font-family:Verdana, Arial, Helvetica, sans-serif;text-decoration:none;text-align:right;align:right;">More</a>
<?
pg_close($dbcon);
?>
</div>

