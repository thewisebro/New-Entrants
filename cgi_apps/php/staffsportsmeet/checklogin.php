<?php
    session_start();
    $username=$_POST["myusername"];
    $password=$_POST["mypassword"];

    if (($username=="admin") && $password=="sp0rtsm33t")
    {
        session_regenerate_id();
        $_SESSION['loggedin'] = true;
	session_write_close();
	header('location:index.php');
    }
    else
    {
	header('location:login.php?loginerror=1');
    }
?>
