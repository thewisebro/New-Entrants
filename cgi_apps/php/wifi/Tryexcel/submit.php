<html>
	<head>
		<title>Form submitted</title>
	</head>

<body>
<?php
include("conn.php");
error_reporting(E_ALL);
$userid = $_POST["username"];
echo $userid;
$result = pg_query($regol,"SELECT * from person_view where person_id='$userid'");
$row = pg_fetch_array($result);
pg_close($regol);
$enrol=$row['enrollment_no'];
echo $enrol;
$name = $row['name'];
$email =$userid."@iitr.ernet.in";
$password = md5($_POST["password"]);
$mac1 = $_POST["mac1"];
$mac2 = $_POST["mac2"];
$mac3 = $_POST["mac3"];
$mac4 = $_POST["mac4"];
$mac5 = $_POST["mac5"];
$mac6 = $_POST["mac6"];
$mac = $mac1.'-'.$mac2.'-'.$mac3.'-'.$mac4.'-'.$mac5.'-'.$mac6;
$roomno = $_POST["roomno"];
echo $roomno;
$bhawan = $_POST["bhawan"];
$mobile = $_POST["mobile"];
$sid = $_POST["sid"];
$uid = $_POST["uid"];
$time= date('Ymd');
echo $time;
$cheok=pg_query($dbcon,"SELECT * FROM session_id where username='$userid'");
$check2=pg_fetch_array($check);
$sessionid=$check2['sessionid'];
//$check_get=pg_fetch_row($check);
//if($check_get[0])
/*if($sessionid==$sid)
{$login=1;}
}
else $login=-1;

if ($login==1)
{
*/
$verify=pg_query($dbcon,"SELECT * from wifimac where username='$userid'");
$previous=pg_fetch_array($verify);
if($userid==$previous['username'])
{
$delete=pg_query($dbcon,"DELETE from wifimac where username='$userid'");
}
else{
$sql = "INSERT INTO wifimac(name,enrol,email,password,mac,roomno,bhawan,mobile,username) values('$name','$enrol','$email','$password','$mac','$roomno','$bhawan','$mobile','$userid','$time');";
pg_query($dbcon,$sql);
}
pg_close($dbcon);
//header("Location: receipt.php?username=$userid&sessionid=$sid");
/*}
else
{
	echo "Not logged in";
}*/
?>

</body>

</html>

