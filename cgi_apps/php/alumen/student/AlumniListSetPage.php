<?php
session_start();
$_SESSION['al_page']=$_GET['page'];
?>
<script type="text/javascript">
document.location.hash="";
document.location.href="../student.php#Mentorship";
</script>

