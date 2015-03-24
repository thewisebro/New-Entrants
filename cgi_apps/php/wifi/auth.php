<?php
require("func.php");
if(pop_authenticate($username,$password,"192.168.121.26"))
{
session_create($username,null);
header("Location: faculty.php?username=$username");
}

else if($sessionid)
{
session_create($username,$sessionid);
header("Location: faculty.php?username=$username");
}

else
{
header("Location: index.php?temp=l");
}
?>
