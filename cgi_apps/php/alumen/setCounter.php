<?php 
require('connection.php');
$submit_query="update emails set email_ids='',counter=10";
pg_query($dbcon,$submit_query);
?>
