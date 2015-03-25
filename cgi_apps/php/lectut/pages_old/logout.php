<?php

header("Location: /nucleus/logout");

/*include("../common/database.php");
session_start();

$username=$_SESSION['username'];

database::connectToDatabase("intranet5");

$query="delete from session_id where username='$username';";
if (database::executeQuery("intranet5",$query))
{ 
	session_destroy();
 	header("Location: index.php?temp=p");
}
else
{
	echo "There occured some problem while logging you out. Please try again.";
}

database::closeDatabase("intranet5");
*/
?>
