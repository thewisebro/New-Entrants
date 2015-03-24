<?php
include_once('../session/django_session.php');
//include_once('../session/util.php');

function islogin()
{
//$query="Select sessionid from session_id where username='$username' and sessionid='$sessionid';";
//$result=pg_query($dbcon,$query);
$session=new Session();

if($session->isLoggedin())
{
  global $userid, $telnet;
  $userid=$session->get_username();
  $telnet = $session->get_userid();
  echo $telnee;
  //var_dump($userid);
	return true;
}
else
	return false;
}
?>
