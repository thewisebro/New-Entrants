<?php

$id = $_GET['id'];
$const = "http://channeli.in/notices/data/n";
$lines = file($const.$id);
foreach ($lines as $line) {
    echo htmlspecialchars($line);
    }
?>
