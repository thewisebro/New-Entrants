<?php
?>
<span class="header">Registration Complete!</span>
<p><span class="header">Next Steps:</span><br/>
Your status as an alumni of IIT Roorkee will be verified as per the details filled by you (<b>Step 1</b>). Once verified you will be sent an invitation to participate in this Mentorship Programme. You may edit the details filled in <b>Step 2</b> by logging into this portal again. Thank you for taking out time to register.</p>

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
