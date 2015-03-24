<?php
session_start();
session_unset();
unset($_SESSION["admin_user"]);
session_destroy();

header("Location: index.html");
?>
