<?php
header('Content-type: text/xml');
include('../db_connection.php');
include('../authenticate.php');

$catg_code = $_POST['catg_code'];
$search = $_POST['search_item'];
$limit = $_POST['limit'];
$username = $_POST['user'];
$password = stripslashes(urldecode($_POST['pass']));

$login = authenticate($username,$password);

if($login==1) {
if($catg_code=="All") {
$sql = "SELECT id,date,subject,sent_from,sent_to FROM notices WHERE subject ILIKE '%".$search."%' OR date ILIKE '%".$search."%' ORDER BY id DESC LIMIT ".$limit;
}
else
$sql = "SELECT id,date,subject,sent_from,sent_to FROM notices WHERE sent_to ILIKE '%".$catg_code."%' AND (subject ILIKE '%".$search."%' OR date ILIKE '%".$search."%') ORDER BY id DESC LIMIT ".$limit;
$result = pg_query($sql);
$count = pg_num_rows($result);

echo "<notices count='".$count."' login='true'>";
while($row = pg_fetch_assoc(($result))) {
        echo "
		<notice>
	      		<id>".$row['id']."</id>
	      		<subject>".$row['subject']."</subject>
	      		<date>".$row['date']."</date>
	      		<sent_from>".$row['sent_from']."</sent_from>
			<sent_to>".$row['sent_to']."</sent_to>
	      	</notice>";
}

echo "</notices>";
}
else
echo "<notices count='0' login='false'></notices>";
?>
