<?php
    require_once("auth.php");
    include("connection.php");

    $error=false;
    $error_message="";

    $dbconn=getConnection();

    if (!(isset($_POST["selectphoto"])))
    {
        $result = pg_query($dbconn,"SELECT old_location FROM convo13_photos;");
        if (!$result)
	{
            $error=true;
            $error_message="An error occured.\n";
            exit;
	}
?>
<!doctype html>
<html>

<form action="delete.php" method="post">

  <b>Select photo : </b>
  <select name="selectphoto">
<?php
    while ($row = pg_fetch_row($result)) {
?>
    <option value="<?php echo $row[0];?>">
      <?php echo "$row[0]"; ?>
    </option>
<?php
    }
?>

<input type="submit" value="Delete Photo">
</form>

<?php
    }

    else
    {
        pg_query($dbconn,"DELETE FROM convo13_photos where old_location='".$_POST['selectphoto']."';");
	shell_exec('rm '.$_POST['selectphoto']);

	$result1 = pg_query($dbconn,"SELECT old_location FROM convo13_photos;");
	if (!$result1)
	{
	    $error=true;
	    $error_message="An error occured.\n";
	    exit;
	}
?>

<form action="delete.php" method="post">

  <b>Select photo : </b>
  <select name="selectphoto">

<?php

    while ($row= pg_fetch_row($result1))  
    {
?>
    <option value="<?php echo $row[0]; ?>">
      <?php echo $row[0]; ?>
    </option>
<?php	
    }
?>
  </select>
  <input type="submit" value="Delete Photo">
</form>
<p>
<?php
    echo "Photo Deleted"; 
}
?>


<form action="index.php">
  <input type="submit" value="Go to Picture View">
</form>
<p>
</html>
