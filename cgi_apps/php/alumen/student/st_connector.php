<?php
session_start();
$_SESSION['viewstudent']=$_GET['student'];
?>
<script type="text/javascript">
document.location.hash="";
document.location.href="../loginSuccess.php#ViewStudentProfile";
</script>

