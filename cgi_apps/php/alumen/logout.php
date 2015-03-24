<?php
session_start();
session_unset();
session_destroy();

header("Location: index.php#Introduction");
die();
?>
<script type="text/javascript">
document.location.hash="";
document.location.href="index.php#Introduction";
</script>
