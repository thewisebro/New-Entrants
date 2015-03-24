<?php
$a = 'hello';
// make a connection
$var = mysqli_connect("192.168.121.9","equip","equ!p","channeli");
if(!$var)

// Check connection
if (mysqli_connect_errno($var))
    {
        echo "Failed to connect to MySQL :bad luck ";
    }
else 
    {
        echo " connection success yippee";
       
    }
?>

