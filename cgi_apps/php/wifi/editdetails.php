<html>
<head>
<title>
Wi-Fi Registration, ISC
</title>
<script language="JavaScript" src="gen_validatorv31.js" type="text/javascript"></script>
<link rel="stylesheet" type="text/css" href="style.css" />
<style>
BODY, P,TD{ font-family: Trebuchet MS, Verdana,Helvetica,sans-serif; font-weight:bold; font-size: 10pt }
A{font-family: Trebuchet MS,Verdana,Helvetica, sans-serif;}
B {	font-family : Trebuchet MS, Helvetica, sans-serif;	font-size : 12px;	font-weight : bold;}
.error_strings{ font-family:Verdana; font-size:10px; color:#660000;}
</style>

</head>

<body>

<?
//error_reporting(E_ALL);
//$sid=$_GET["sessionid"];
//$userid=$_GET["username"];
//$user=$_GET["user"];
include("conn.php");
include("login_check.php");
?>

<?
if(islogin()== false)	//redirect the user to login page if he is not loggd in
	//even if he is somehow not logged in show him the link to do so
{
header("Location: /nucleus/login/?next".$_SERVER['REQUEST_URI']); 
}
//mysql_close($regol);
//mysql_close($dbcon);
?>
<div id="container">&nbsp;
<div id="header">
<p id="header_text">Wi-Fi/Lan Registration </p>
<!--<img src="images/header.jpg" alt="WI-Fi logo">-->
</div>
<div id="main">
<?
$verify=mysql_query("SELECT * from wifimac where enrol='$userid'",$dbcon);

if($previous=mysql_fetch_array($verify))
{
$mac_arr=explode("-",$previous[mac],6);

/*?>
You have already completed your Wi-fi registration, with mac address:<? echo $previous["mac"] ?>.<br><br>
If you want to change it, kindly approach Mr. Naveen Shukla at Information Superhighway Center.
<?
mysql_close($dbcon);
}
else {
*/?>
<form action="submitcheck.php" name="WifiMain" method="post" >
<table>
<tr>
   <td>Username </td>
   <td> <input type="text" value="<? print($previous[username]) ?>" readonly="readonly" name="username"> </td>
</tr>
<tr>
   <td>Password</td>
   <td> <input type="password" name="password" value=<? print($previous[password]) ?> /><b>*Need not be same as webmail</b></td>
</tr>
<tr>
   <td>Confirm Password</td>
   <td> <input type="password" name="password_c" value=<? print($previous[password]) ?> /></td>
</tr>
<tr>

   <td>MAC/Physical Address</td>
   		<td><input type="text" name="mac1" size="2" maxlength="2" value=<? echo $mac_arr[0]; ?> />
                <input type="text" name="mac2" size="2" maxlength="2" value=<? echo $mac_arr[1]; ?> />
                <input type="text" name="mac3" size="2" maxlength="2" value=<? echo $mac_arr[2]; ?> />
                <input type="text" name="mac4" size="2" maxlength="2" value=<? echo $mac_arr[3]; ?> />
                <input type="text" name="mac5" size="2" maxlength="2" value=<? echo $mac_arr[4]; ?> />
                <input type="text" name="mac6" size="2" maxlength="2" value=<? echo $mac_arr[5]; ?> /></td>
</tr>
<tr>
	<td>Room Number</td>
	<td><input type="text" name="roomno" value="<? echo $previous[roomno]; ?>" /></td>
</tr>
<tr>
	<td>Bhawan</td>
         <td>
	 <select name="bhawan">
	 <? $selected1="";$selected2="";$selected3="";
	 	if ($previous[bhawan]=="Sarojini") $selected3="selected"; 
	 	elseif ($previous[bhawan]=="Kasturba") $selected2="selected";
		else $selected1="selected";

	 ?>
	 	<option value="" <? echo $selected1; ?>>[choose yours]
                       <option value="Kasturba" <? echo $selected2; ?>>Kasturba</option>
                       <option value="Sarojini" <? echo $selected3; ?>>Sarojini</option>
		       <option value="Rajendra" <? echo $selected4; ?>>Rajendra</option>
                       <option value="Ravindra" <? echo $selected5; ?>>Ravindra</option>
		       <option value="Govind" <? echo $selected6; ?>>Govind</option>
		       <option value="Azad" <? echo $selected7; ?>>Azad</option>
                       <option value="Jawahar" <? echo $selected8; ?>>Jawahar</option>
                       <option value="Ganga" <? echo $selected9; ?>>Ganga</option>
                       <option value="Cautley" <? echo $selected10; ?>>Cautley</option>



         </select>
	 </td>
</tr>
<tr>
         <td>Mobile Number</td>
	 <td><input type="text" name="mobile" value="<? echo $previous[mobile]; ?>" /></td>
</tr>
<tr>
<td>
<input type="hidden" name="sessionid" value="<? print($sid) ?>" />
<input type="hidden" name="user" value="<? print($user) ?>" />
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
  frmvalidator.addValidation("password","req","Please enter your webmail password");
   
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
}
mysql_close($dbcon);
?>
</div>
<div id="footer">
Credits: Information Management Group.<br>
Copyright &copy; IMG, ISC, IIT Roorkee, 2010.
</div>

</div>
</body>
</html>
