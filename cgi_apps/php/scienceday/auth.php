<?php
    session_start();

    if(!isset($_SESSION['loggedin']) || (trim($_SESSION['loggedin']) == ''))
    {
        header("location: login.php?nologin=1");
        exit();
    }
?>

