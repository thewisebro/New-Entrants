<?php
    //Start session
    session_start();

    //Unset the variables stored in session
    unset($_SESSION['loggedin']);
    header("location: index.php");
?>
