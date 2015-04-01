<html>
	<head><link rel="stylesheet" type="text/css" href="style.css" />
		<title>Wifi Registration...</title>
		<style>
		table,tr,td { border:solid 1px #000; }
		</style>
	</head>

<body>
<?php
//error_reporting(E_ALL);
//$userid=$_GET["username"];
include("conn.php");
include("login_check.php");
?>
<?
if( islogin()== false)	//redirect the user to login page if he is not loggd in
	//even if he is somehow not logged in show him the link to do so
{
header("Location: /nucleus/login/?next=".$_SERVER['REQUEST_URI']);
} 
?>
<div id="container">
&nbsp;
<div id="header">
<p id="header_text">Wi-Fi/Lan Registration </p>
<!--<img src="images/header.jpg" alt="WI-Fi logo">-->
</div>
<div id="main">

<?
//error_reporting(E_ALL);
//$sid = $_POST["sessionid"];
//$userid = $_POST["username"];
//echo $userid;
$result = mysql_query("SELECT e.person_id,p.name from nucleus_personidenrollmentnomap e,nucleus_person p,auth_user a where a.username='$userid' and a.id=p.user_id and e.enrollment_no='$userid'");
$row = mysql_fetch_array($result);
$enrol=$userid;
$name = $row['name'];
$email =$row['person_id']."@iitr.ernet.in";
$password = $_POST["password"];
$mac1 = strtoupper($_POST["mac1"]);
$mac2 = strtoupper($_POST["mac2"]);
$mac3 = strtoupper($_POST["mac3"]);
$mac4 =strtoupper($_POST["mac4"]);
$mac5 =strtoupper($_POST["mac5"]);
$mac6 =strtoupper($_POST["mac6"]);
$mac = $mac1.'-'.$mac2.'-'.$mac3.'-'.$mac4.'-'.$mac5.'-'.$mac6;
$roomno = strtoupper($_POST["roomno"]);
$bhawan = $_POST["bhawan"];
$mobile = $_POST["mobile"];
//$sid = $_POST["sid"];
//$uid = $_POST["uid"];
$time= date('Ymd');
?>
<p>Please check whether the following details are correct:</p>
<form action="submit.php" method="post">
<table border="0" cellspacing="0">

<tr>
	<td>Name</td>
	<td><? echo $name ?></td>
</tr>
<tr>
	<td>E-mail id</td>
	<td><? echo $email ?></td>
</tr>
<tr>
	<td>Enrollment No</td>
	<td><? echo $enrol ?></td>
</tr>

<tr>
	<td>MAC Address</td>
	<td><? echo $mac ?></td>
</tr>
<tr>
	<td>Room No</td>
	<td><? echo $roomno ?></td>
</tr>
<tr>
	<td>Bhawan</td>
	<td><? echo $bhawan ?></td>
</tr>
<tr>
	<td>Mobile No</td>
	<td><? echo $mobile ?></td>
</tr>
<tr>
	<td>Date of this submission</td>
	<td><? echo $time ?></td>
</tr>
</table>


<input type="hidden" name="username" value="<? print($userid) ?>">
<input type="hidden" name="name" value="<? print($name) ?>">
<input type="hidden" name="email" value="<? print($email) ?>">
<input type="hidden" name="mac" value="<? print($mac) ?>">
<input type="hidden" name="roomno" value="<? print($roomno) ?>">
<input type="hidden" name="bhawan" value="<? print($bhawan) ?>">
<input type="hidden" name="mobile" value="<? print($mobile) ?>">
<input type="hidden" name="time" value="<? print($time) ?>">
<input type="hidden" name="enrol" value="<? print($enrol) ?>">
<input type="hidden" name="password" value="<? print($password) ?>">
<input type="hidden" name="user" value="<? echo 'naveen';?>">
<br><br><div>If the details are correct, then please
<input type='submit' name='Submit' value='Submit'>
</div>
<br><br>
<? if ($_POST[user]=="naveen") { ?>
If you want to modify any details, please <a href="editdetails.php">Click Here</a>.<br>

<? } else { ?>
If you want to modify any details, please <a href="index.php">Click Here</a>.<br>
<? } ?>
<br>
</div>
<div id="footer">
Credits: Information Management Group.<br>
Copyright &copy; IMG, ISC, IIT Roorkee, <? echo date("Y"); ?>.
</div>

</div>
</body>

</html>

