
<html>
<head>
</head>

<body>

<?
$sid=$_GET[sid];
$userid=$_COOKIE["username"];
include("conn.php");
?>
 <form name="WifiMain" action="submit.php" method="post">
<table >
<tr>
   <td>Username </td>
   <td> <input type="text" name="username"> </td>
</tr>
<tr>
   <td>Password</td>
   <td> <input type="password" name="password" /><b>*Need not be same as webmail</b></td>
</tr>
<tr>
   <td>Confirm Password</td>
   <td> <input type="password" name="password_c" /></td>
</tr>
<tr>

   <td>MAC/Physical Address</td>
   		<td><input type="text" name="mac1" size="2"/>
                <input type="text" name="mac2" size="2" />
                <input type="text" name="mac3" size="2"/>
                <input type="text" name="mac4" size="2"/>
                <input type="text" name="mac5" size="2"/>
                <input type="text" name="mac6" size="2"/></td>
</tr>
<tr>
	<td>Room Number</td>
	<td><input type="text" name="roomno" /></td>
</tr>
<tr>
	<td>Bhawan</td>
         <td>
	 <select name="bhawan">
                       <option value="Kasturba">Kasturba</option>
                       <option value="Sarojini">Sarojini</option>
         </select>
	 </td>
</tr>
<tr>
         <td>Mobile Number</td>
	 <td><input type="text" name="mobile" /></td>
</tr>
 
<tr><td><input type="submit" name="submit"  value="submit"></td></tr>
</table>


</body>
</html>
