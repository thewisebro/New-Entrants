<?php

function db() {
  $con = mysql_connect("192.168.121.5","channeli","channeli");
  if (!$con) {
    die('Could not connect: ' . mysql_error());
  }

  mysql_select_db("channeli", $con);

  return $con;
}

?>
