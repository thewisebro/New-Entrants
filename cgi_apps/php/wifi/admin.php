<html>
	<head>
		<title>Registered Students</title>
<script language="JavaScript" src="gen_validatorv31.js" type="text/javascript"></script>
<link rel="stylesheet" type="text/css" href="style.css" />
<style>
BODY, P,TD{ font-family: Trebuchet MS, Verdana,Helvetica,sans-serif;}
A{font-family: Trebuchet MS,Verdana,Helvetica, sans-serif;}
B {	font-family : Trebuchet MS, Helvetica, sans-serif;	font-size : 12px;	font-weight : bold;}
.error_strings{ font-family:Verdana; font-size:10px; color:#660000;}
</style>
	</head>
<?php
/**********************************************************************/
/*** To see the registered students details by various search and export search result in Excel formal********/
/******By CS Vikram*********************************/
/**********************************************************************/
//$sid=$_GET["sessionid"];
//$userid=$_GET["username"];
include("conn.php");
include("login_check.php");

if(islogin()== false)	//redirect the user to login page if he is not loggd in
	//even if he is somehow not logged in show him the link to do so
{
header("Location: /nucleus/login/?next".$_SERVER['REQUEST_URI']);

}
if($userid!= "naveen")
{
  header('Location: /');
}


?>
<body>
<div id="container">&nbsp;
<div id="header">
<p id="header_text">Wi-Fi/Lan Registration </p>
<!--<img src="images/header.jpg" alt="WI-Fi logo">-->
</div>
<div id="main">

<form name="WifiMain" action="result1.php" method="POST">
<table >
<tr>
	<td>Select Bhawan : </td><td><input name="bhawan[]" type="checkbox" value="Azad">Azad</input></td>
</tr><tr>
	<td><input name="bhawan[]" type="checkbox" value="Kasturba">Kasturba</input></td>
	<td><input name="bhawan[]" type="checkbox" value="Sarojini">Sarojini</input></td></td>
</tr><tr>
	<td><input name="bhawan[]" type="checkbox" value="Govind">Govind</input></td>
	<td><input name="bhawan[]" type="checkbox" value="Ravindra">Ravindra</input></td>
</tr><tr>
	<td><input name="bhawan[]" type="checkbox" value="Rajendra">Rajendra</input></td>
	<td><input name="bhawan[]" type="checkbox" value="Jawahar">Jawahar</input></td>
</tr><tr>
	<td><input name="bhawan[]" type="checkbox" value="Radhakrishna">Radhakrishna</input></td>
	<td><input name="bhawan[]" type="checkbox" value="Rajiv">Rajiv</input></td>
</tr><tr>
	<td><input name="bhawan[]" type="checkbox" value="Ganga">Ganga</input><br/><br/></td>
	<td><input name="bhawan[]" type="checkbox" value="Cautley">Cautley</input><br/><br/></td>
</tr>

<tr>
	<td><input type="radio" name='flag' value='name' checked=""></input>
	Search by Name
	<td><input type="text" name="name">
</tr>
<tr>
	<td><input type="radio" name='flag' value='username'></input>
	Search by Username 
	<td><input type="text" name="username"></td>
</tr>
<tr>
	<td><br>
	<input type="radio" name='flag' value='date'></input>
	Search by Date
<tr>
 <tr>
   <td>Starting Date </td>
   <td>
<input type="text" name="init_date" value="dd/mm/yyyy" size="15" maxlength="10"> 
	<input type="button" name="cmdCal" value="Launch Calendar" onClick='javascript:window.open("calendar.php?form=WifiMain&field=init_date","","top=50,left=400,width=175,height=140,menubar=no,toolbar=no,scrollbars=no,resizable=no,status=no"); return false;'>
  </td>
</tr>
<tr>
   <td>Final Date </td>
   <td>
<input type="text" name="final_date" value="dd/mm/yyyy" size="15" maxlength="10"> 
	<input type="button" name="cmdCal" value="Launch Calendar" onClick='javascript:window.open("calendar.php?form=WifiMain&field=final_date","","top=50,left=400,width=175,height=140,menubar=no,toolbar=no,scrollbars=no,resizable=no,status=no"); return false;'>
  </td>
</tr>
<tr>
	<td><br><input type="radio" name='flag' value='mac'></input>
	Search by Mac
<tr>
</tr>
<tr>
   <td>MAC/Physical Address</td>
   <td> <input type="text" name="mac1" maxlength="2" size="2"/>
        <input type="text" name="mac2" maxlength="2" size="2"/>
	<input type="text" name="mac3" maxlength="2" size="2"/>
	<input type="text" name="mac4" maxlength="2" size="2"/>
        <input type="text" name="mac5" maxlength="2" size="2"/>
        <input type="text" name="mac6" maxlength="2" size="2"/>
	<input type="hidden" name="user" value="naveen" />
</td>
 </tr>
 <tr><td><br><input type="submit" name="submit"  value="Edit Details"><input type="submit" name="excel" value="Generate Excel File" /></td></tr>
<tr><td>	<div id='WifiMain_errorloc' class='error_strings'>
	                              </div>
</td></tr>
</table>
</form>
<script language="JavaScript" type="text/javascript">
//You should create the validator only after the definition of the HTML form
  var frmvalidator  = new Validator("WifiMain");
   frmvalidator.EnableOnPageErrorDisplaySingleBox();
    frmvalidator.EnableMsgsTogether();
 frmvalidator.addValidation("bhawan","dontselect=0");
</script>
</div>
<div id="footer">
Credits: Information Management Group.<br>
Copyright &copy; IMG, ISC, IIT Roorkee, 2014.
</div>

</div>
</body>

</html>

