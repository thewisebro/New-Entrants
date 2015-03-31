<?php
session_start();
if(($_POST["username"]=="ajay" && $_POST["password"]=="m!nutes" ) || ($_SESSION["username"]=="ajay" && $_SESSION["password"]=="m!nutes" ))
{
	$_SESSION["username"]="ajay";
	$_SESSION["password"]="m!nutes";
	header("location:upload.php");
}
else if(($_POST["username"]=="dairy" && $_POST["password"]=="m!lkfood" ) || ($_SESSION["username"]=="dairy" && $_SESSION["password"]=="m!lkfood" ))
{
	$_SESSION["username"]="dairy";
	$_SESSION["password"]="m!lkfood";
	header("location:upload_dairy.php");
}

else
{
?>
<b>Meeting Minutes</b>
<form action="login.php" method="POST">
Username:<input type="text" name="username" /><br/>
Password:<input type="password" name="password" /><br/>
<input type="submit" name="submit" value='Login' /><br/>
</form>
<?php
}
?>
