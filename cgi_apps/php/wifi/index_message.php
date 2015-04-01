<?php
error_reporting(E_ALL);
include("conn.php");
include("login_check.php");
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
<link href='https://fonts.googleapis.com/css?family=Roboto+Slab' rel='stylesheet' type='text/css'>
</head>
<body style="text-align: center;height: 800px;line-height: 450px;font-family: 'Roboto Slab', serif;font-size: 35px;">
LAN registration is closed now..
</body>
</html>
