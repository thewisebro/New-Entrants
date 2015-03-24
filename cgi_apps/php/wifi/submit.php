<html>
	<head><link rel="stylesheet" type="text/css" href="style.css" />
		<title>Wifi Registration Succesful</title>
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
<?/*
if( islogin($userid,$sid,$dbcon)== false)	//redirect the user to login page if he is not loggd in
	//even if he is somehow not logged in show him the link to do so
{
?>
	<script type="text/javascript" >
		window.location="http://192.168.121.7/commonLogin/login.do";
	</script>
	<a href="http://192.168.121.7/commonLogin/login.do">PLEASE LOGIN</a>
 
<?
}
mysql_close($dbcon);
*/?>

<?
function email_to_user($to, $from='noreply@iitr.ernet.in', $subject='No Subject', $messagetext='hello', $messagehtml='testing', $fromname='', $fname1='', $fname2='', $fname3='')
{
$usetrueaddress=true;
include_once('./phpmailer/class.phpmailer.php');
$mail = new phpmailer;
$mail->PluginDir = './phpmailer/';
$mail->CharSet = 'UTF-8';
$mail->IsSMTP();
$mail->Host = '192.168.121.26';
$mail->SMTPAuth = false;
$mail->From = $from;
$mail->FromName = $fromname;
$mail->AddReplyTo('noreply@iitr.ernet.in','NO REPLY');
$mail->Subject = substr(stripslashes($subject), 0, 900);
$mail->AddAddress($to); // now, i'll have to check if this works for multiple mails, or do i have to do a for loop, or if calling this multiple times, adds multiple users...

// BCC to neha1umt@iitr.ernet.in for testing purpose
//$mail->AddBCC('bcc4groupmail@gmail.com','Neha');
$mail->AddAttachment('/home/apps/php/groupmailer/temp_loc/'.$fname1,$fname1);
$mail->AddAttachment('/home/apps/php/groupmailer/temp_loc/'.$fname2,$fname2);
$mail->AddAttachment('/home/apps/php/groupmailer/temp_loc/'.$fname3,$fname3);
$mail->WordWrap = 79;
$mail->IsHTML(true);
$mail->Encoding = 'quoted-printable';
$mail->Body    =  $messagehtml;
$mail->AltBody =  "\n$messagetext\n";
$mail->Send();
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
$password = $_POST["password"];
$mac = strtoupper($_POST["mac"]);
$userid = $_POST["username"];
$enrol = $_POST["enrol"];
$time = $_POST["time"];
$email = $_POST["email"];
$roomno = $_POST["roomno"];
$bhawan = $_POST["bhawan"];
$mobile = $_POST["mobile"];
$name = $_POST["name"];
//error_reporting(E_ALL);
//$uid = $_POST["uid"];
$time= date('Ymd');
if ($_POST[user]=='naveen') {
mysql_query($dbcon,"DELETE FROM wifimac where username='$userid'");
}
$verify=mysql_query("SELECT * from wifimac where username='$userid'",$dbcon);
$previous=mysql_fetch_array($verify);
$num=mysql_num_rows($verify);
if($num>0)
{
  $verify_mac=mysql_query("Select * from wifimac where mac='$mac'",$dbcon);
  $previous_mac=mysql_fetch_array($verify_mac);
  $num_mac=mysql_num_rows($verify_mac);
  if($num_mac>0 && $previous_mac['username']!=$userid)
  {
      echo '<p>The Mac address provided by you is already registered. Please confirm it once. If you are entering correct MAC address, then approach Naveen Shukla at ISC.</div>';
  }
  else
  {
    // UPDATE
    $update_query = "UPDATE wifimac SET name='$name', enrol='$enrol', email='$email', password='$password', mac='$mac', roomno='$roomno', bhawan='$bhawan', mobile='$mobile', username='$userid', registered_date='$time'  where username='$userid';";
    mysql_query($update_query,$dbcon);
   //   var_dump($update_query);
     echo '<div style="min-height:250px;">Your changes have been updated</div>';
  }

mysql_close($dbcon);
// <!--<p>The Mac address provided by you is already registered. Please confirm it once. If you are entering correct MAC address, then approach Naveen Shukla at ISC.</div>-->
}
else{
$sql = "INSERT INTO wifimac(name,enrol,email,password,mac,roomno,bhawan,mobile,username,registered_date) values('$name','$enrol','$email','$password','$mac','$roomno','$bhawan','$mobile','$userid','$time');";
//var_dump($sql);
mysql_query($sql,$dbcon);

mysql_close($dbcon);
//header("Location: receipt.php?username=$userid&sessionid=$sid");
/*
else
{
	echo "Not logged in";
}*/
?>
<p>Following details has been successfully submitted. </p>
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

<? $email_data="
<table border='0' cellspacing='0'>

<tr>
	<td>Name</td>
	<td>$name</td>
</tr>
<tr>
	<td>E-mail id</td>
	<td>$email</td>
</tr>
<tr>
	<td>Enrollment No</td>
	<td>$enrol</td>
</tr>

<tr>
	<td>Password</td>
	<td>$password</td>
</tr>

<tr>
	<td>MAC Address</td>
	<td>$mac</td>
</tr>
<tr>
	<td>Room No</td>
	<td>$roomno</td>
</tr>
<tr>
	<td>Bhawan</td>
	<td>$bhawan</td>
</tr>
<tr>
	<td>Mobile No</td>
	<td>$mobile</td>
</tr>
<tr>
	<td>Date of this submission</td>
	<td>$time</td>
</tr>
</table> ";

$subject="Wi-Fi Registration";
?>
<? 
email_to_user($email,"img@iitr.ernet.in",$subject,"hello",$email_data);
 }
?>
<br><br>
Return to <a href="/" >Channel I</a>
</div>
<div id="footer">
Credits: Information Management Group.<br>
Copyright &copy; IMG, ISC, IIT Roorkee, 2014.
</div>


</div>
</body>

</html>

