<?php
require_once("auth.php");
?>
<!doctype html>
<html>
<head>
<script type="text/javascript">
var upload_number = 2;
function addFileInput() {
 	var d = document.createElement("div");
 	var file = document.createElement("input");
 	file.setAttribute("type", "file");
 	file.setAttribute("name", "ufile"+upload_number);
 	d.appendChild(file);
 	document.getElementById("moreUploads").appendChild(d);
 	upload_number++;
	document.getElementById("number").value = upload_number;
}

</script>
</head>
<form action="upload_file.php" method="post" enctype="multipart/form-data">
<label for="file">Filename : </label>
<input type="file" name="ufile1" id="ufile" onchange="document.getElementById('moreUploadsLink').style.display='block';" />
<div id="moreUploads"></div>
<div id="moreUploadsLink" style="display:none;"><a href="javascript:addFileInput();">Attach another File</a></div>
<br />
<div></div>
<input type="submit" value="Submit" name="submit">
<input type="hidden" name="number" id="number" value="1" />
</form>
<form action="index.php">
<input type="submit" value="Go to the Picture View"/>
</form>
<?php
?>
</html>
