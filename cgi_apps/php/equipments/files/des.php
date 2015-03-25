<?php
$fruit = array('a' => 'apple', 'b' => 'banana', 'c' => 'cranberry');
//reset($fruit);
while (list($key, $val) = each($fruit)) {
      echo "$key => $val\n";
}
?>

