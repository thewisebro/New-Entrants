<?php
header('Content-type: text/xml');
include('../db_connection.php');
include('../authenticate.php');


$param = isset($_POST['catg_code']) ? $_POST['catg_code'] : null;
$id = isset($_POST['id']) ? $_POST['id'] : null;
$limit = isset($_POST['limit']) ? $_POST['limit'] : 10;
$username = $_POST['user'];
$password = $_POST['pass'];
$password = stripslashes(urldecode($password));

/*
$limit = 10;
$username = "lalitumt";
$password = '768528Aa"';
$password = stripslashes(urldecode($password));
*/

//$login = authenticate($username,$password);

if(TRUE) {

if(TRUE)
	$sql = "SELECT id,date,subject,sent_from,sent_to FROM notices ORDER BY id DESC LIMIT ".$limit;

else if($param==null && $id!=null)
	$sql = "SELECT id,date,subject,sent_from,sent_to FROM notices WHERE id> ".$id." ORDER BY id DESC LIMIT ".$limit;

else if($param!=null && $id==null)
	$sql = "SELECT id,date,subject,sent_from,sent_to FROM notices WHERE sent_to LIKE '%".$param."%' ORDER BY id DESC LIMIT ".$limit;
else if($param!=null && $id!=null)
	 $sql = "SELECT id,date,subject,sent_from,sent_to FROM notices WHERE sent_to LIKE '%".$param."%' AND id > ".$id." ORDER BY id DESC LIMIT ".$limit;

$result = pg_query($conn, $sql);
$count = pg_num_rows($result);

echo    "<notices count='".$count."' login='true'>";
while($row = pg_fetch_assoc(($result))) {
        echo "
		<notice>
			<id>".htmlentities($row['id'])."</id>
			<subject>".htmlentities($row['subject'])."</subject>
			<date>".htmlentities($row['date'])."</date>
			<sent_from>".htmlentities($row['sent_from'])."</sent_from>
			<sent_to>".htmlentities($row['sent_to'])."</sent_to>
		</notice>";
}

echo "
</notices>";
}

else
	echo "<notices count='1' login='false'></notices>";
?>
