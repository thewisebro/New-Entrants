<form action="changePasswordPost.php" method="post" onsubmit="if(this.new_password.value!=this.confirm_password.value){alert('Passwords(new) do not match');return false;}">
<table border="0">
<tr>
<td>Old Password</td>
<td><input type="password" name="old_password"></td>
</tr>

<tr>
<td>New Password</td>
<td><input type="password" name="new_password"></td>
</tr>

<tr>
<td>Confirm New Password</td>
<td><input type="password" name="confirm_password"></td>
</tr>

</table>
<br/>
<input type="submit" value="Change Password">
</form>
