<?php
session_start();
error_reporting(0);

?>


<form method="post" action="suggestionPost.php">
<?
if(isset($_SESSION["username"])){
?>
<input type="hidden" name="username" value="<?echo $username;?>">
<?
}
else
{
?>
<span class="header">Email:</span><br/>
<input type="text" name="username" value="">
<?
}
?>
<span class="header">Your suggestions for making the programme a success</span>
<br/>
<textarea name="suggestion" rows="5" cols="40"></textarea>
<br/>
<input type="submit" value="Submit">
</form>
