<?php
header('Content-type: text/html');
if(isset($_GET['id'])) {
  $id = $_GET['id'];
  $const = "http://channeli.in/notices/data/n";
  $lines = file($const.$id);
  foreach ($lines as $line) {
    echo $line;
  }
}
else
  echo "<h3>Notice Not Found</h3>";
?>

