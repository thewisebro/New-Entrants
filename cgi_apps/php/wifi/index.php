<?php

//header("Location: /wifi/");
error_reporting(E_ALL);
//$sid=$_GET["sessionid"];
//$userid=$_GET["username"];
include("conn.php");
include("login_check.php");
//include("../session/django_session.php");
//$session=new Session();
if(islogin()== false)	//redirect the user to login page if he is not loggd in
	//even if he is somehow not logged in show him the link to do so
{
  header("Location: /nucleus/login/?next=".$_SERVER['REQUEST_URI']);
}
if($userid == "naveen")
{
header('Location: /settings/wifi/ ');
}
?>

<html>
<head>
<title>
Wi-Fi Registration, ISC
</title>
<script language="JavaScript" src="gen_validatorv31.js" type="text/javascript"></script>
<link rel="stylesheet" type="text/css" href="style.css" />
<style>
BODY, P,TD{ font-family: Trebuchet MS, Verdana,Helvetica,sans-serif; font-weight:bold; font-size: 10pt }
a{font-family: Trebuchet MS,Verdana,Helvetica; color:#000; sans-serif;}
B {	font-family : Trebuchet MS, Helvetica, sans-serif;	font-size : 12px;	font-weight : bold;}
.error_strings{ font-family:Verdana; font-size:10px; color:#660000;}
</style>
<script language="JavaScript" type="text/javascript">
function open_win(url_add)
   {
      window.open(url_add,'welcome','width=400,height=300,status=yes,location=yes,toolbar=yes,scrollbars=yes');
   }
</script>
</head>

<body>

 
<?php
if($userid == "naveen")
{
header('Location: /settings/wifi/ ');
}

//var_dump($userid);

?>
<div id="container">&nbsp;
<div id="header">
	<p id="header_text">Wi-Fi/Lan Registration </p>
	<!--<img src="images/header.jpg" alt="WI-Fi logo">-->
</div>
<div id="main">
<?
$verify=mysql_query("SELECT * from wifimac where enrol='$userid'",$dbcon);
$previous=mysql_fetch_array($verify);
if($userid==$previous['enrol'])
{
?>
You have already completed your Wi-fi/LAN registration, with mac address: <? echo $previous["mac"] ?>.<br><br>
<!--If you want you can change it.-->
<?

$mac=$previous['mac'];
$mac=explode("-",$mac);

//mysql_close($dbcon);
}

?>
Note: Here username is your Webmail id. And you must login in Channel i with your Webmail username &amp;
password to fill this form. <br><br>
<form action="submitcheck_first.php" name="WifiMain" method="post" >
<table>
<tr>
   <td>Username </td>
   <td> <input type="text" readonly="readonly" value="<? echo $telnet?>" name="username"> </td>
</tr>
<tr>
   <td>Name </td>
   <td> <input type="text" name="name" value="<? print($previous['name']) ?>" > </td>
</tr>

<tr>
   <td>Enrollment No. </td>
   <td> <input type="text" name="enrol" readonly="readonly" value="<? echo $userid ?>"> </td>
</tr>


<tr>
   <td>Password</td>
   <td> <input type="password" name="password" value="<? print($previous['password']) ?>"/><b>*Need not be same as webmail</b></td>
</tr>
<tr>
   <td>Confirm Password</td>
   <td> <input type="password" name="password_c" value="<? print($previous['password']) ?>"/></td>
</tr>
<tr>

   <td>MAC/Physical Address</td>
   		<td><input type="text" name="mac1" size="2" maxlength="2" value="<? print($mac[0]) ?>"/>
                <input type="text" name="mac2" size="2" maxlength="2"  value="<? print($mac[1]) ?>"/>
                <input type="text" name="mac3" size="2" maxlength="2" value="<? print($mac[2]) ?>"/>
                <input type="text" name="mac4" size="2" maxlength="2" value="<? print($mac[3]) ?>"/>
                <input type="text" name="mac5" size="2" maxlength="2" value="<? print($mac[4]) ?>"/>
                <input type="text" name="mac6" size="2" maxlength="2" value="<? print($mac[5]) ?>"/>
		
<a href="javascript:;" onclick="open_win('howtofind.html')" >How to find Mac Address</a>
</td>
</tr>
<tr>
	<td>Room Number</td>
	<td><input type="text" name="roomno" size="6" value="<? print($previous['roomno']) ?>"/>For Example: F-111</td>
</tr>
<tr>
	<td>Bhawan</td>
         <td>
	 <select name="bhawan" value="Kasturba">
	 	<option value="">[choose yours]
			<option value="Kasturba">Kasturba</option>
			<option value="Sarojini">Sarojini</option>
			<option value="Govind">Govind</option>
			<option value="Ravindra">Ravindra</option>
			<option value="Rajendra">Rajendra</option>
			<option value="Radhakrishna">Radhkrishna</option>
			<option value="Rajiv">Rajiv</option>
			<option value="Ganga">Ganga</option>
			<option value="Cautley">Cautley</option>
			<option value="Jawahar">Jawahar</option>
			<option value="Azad">Azad</option>
	</select>
	 </td>
</tr>
<tr>
         <td>Mobile Number</td>
	 <td><input type="text" name="mobile" value="<? print($previous['mobile']) ?>"/></td>
</tr>
<tr>
<td>
<input type="hidden" name="sessionid" value="<? print($sid) ?>" />
	<div id='WifiMain_errorloc' class='error_strings'>
	                              </div>
				      	</td>

<tr><td><input type="submit" value="Submit"></td></tr>
</table>
</form>

<script language="JavaScript" type="text/javascript">
//You should create the validator only after the definition of the HTML form
  var frmvalidator  = new Validator("WifiMain");
   frmvalidator.EnableOnPageErrorDisplaySingleBox();
   frmvalidator.EnableMsgsTogether();
  frmvalidator.addValidation("password","req","Please enter the password");
   
 frmvalidator.addValidation("mac1","req","Please enter complete MAC number");
 frmvalidator.addValidation("mac1","minlen=2","For MAC address, Min length is 2, for each part.");
 frmvalidator.addValidation("mac2","req","Please enter complete MAC number");
 frmvalidator.addValidation("mac2","minlen=2","For MAC address, Min length is 2, for each part.");
frmvalidator.addValidation("mac3","req","Please enter complete MAC number");
 frmvalidator.addValidation("mac3","minlen=2","For MAC address, Min length is 2, for each part.");
frmvalidator.addValidation("mac4","req","Please enter complete MAC number");
 frmvalidator.addValidation("mac4","minlen=2","For MAC address, Min length is 2, for each part.");
frmvalidator.addValidation("mac5","req","Please enter complete MAC number");
 frmvalidator.addValidation("mac5","minlen=2","For MAC address, Min length is 2, for each part.");
frmvalidator.addValidation("mac6","req","Please enter complete MAC number");
 frmvalidator.addValidation("mac6","minlen=2","For MAC address, Min length is 2, for each part.");
	  
			     frmvalidator.addValidation("mobile","maxlen=10");
  frmvalidator.addValidation("mobile","minlen=10");
			      frmvalidator.addValidation("mobile","numeric");
			        
				    frmvalidator.addValidation("bhawan","dontselect=0");

				    function DoCustomValidation()
				    {
				      var frm = document.forms["WifiMain"];
				        if(frm.password.value != frm.password_c.value)
					  {
					      sfm_show_error_msg('The Password and confirmed password do not match!',frm.password);
					      return false;
					  }
					else
					  {
					   return true;
					  }
				   }
				   frmvalidator.setAddnlValidationFunction("DoCustomValidation");
				    </script>

<?
mysql_close($dbcon);

echo "<a href=\"help.html\"> Download Help File</a>";
//echo "<br/><br/>You are not allowed to visit Channel I ! <br/><a href='http://192.168.121.7/commonLogin/pages/logout.jsp'>LOGOUT</a>";
?>
</div>
<div id="footer">
Credits: Information Management Group.<br>
Copyright &copy; IMG, ISC, IIT Roorkee, <?echo date("Y")?>.
</div>

</div>
</body>

</html>
