<?php
include("connectionFile.php");
$dbcon=getConnection("meeting_minutes","meeting_minutes");

$userid=$_GET["userid"];
$sessionid=$_GET["session_id"];

$query="SELECT sessionid FROM session_id WHERE username='$userid'";

$res=pg_query($dbcon,$query);
$check=false;

while(($row=pg_fetch_array($res))&&!$check){
	if($row['sessionid']==$sessionid)
		$check=true;
}

if(!$check)
	die("You must be logged in to view this page $userid $sessionid");
?>

<html>
	<head>
		<style>
			*
			{
				font-family:'Verdana';
			}
		</style>
	</head>
	<body>
		<b><u>Minutes of BOG meeting</u></b>

		<br/><br/>
		<?php
			$query="SELECT * from meeting_minutes";
			$res=pg_query($dbcon,$query);

			if(pg_num_rows($res)==0){
				echo "No minutes have been uploaded till now<br>";
			}
			else {
				echo "<ul>";	
				
				while($row=pg_fetch_array($res)){
					echo "<li><a href=\"upload/".$row['filename']."\" target=\"_BLANK\">".$row['title']."</a></li>";
				}

				echo "</ul>";

			}

		?>
	</body>

</html>

<?php

pg_close($dbcon);
?>
