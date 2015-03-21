<?php
session_start();
$_SESSION['alumni']=$_GET['alumni'];
?>
<script type="text/javascript">
document.location.hash="";
document.location.href="../student.php#AlumniProfile";
</script>

