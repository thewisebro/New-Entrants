<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>File Uploader</title>
<style type="text/css">
body {
	margin: 10px;
	font: 62% Tahoma, Arial, sans-serif;
}
#main_container{
	font-size: 1.4em;
}
</style>
<link href="css/fileUploader.css" rel="stylesheet" type="text/css" />
<script src="js/jquery-1.4.4.min.js" type="text/javascript"></script>
<script src="js/jquery.fileUploader.js" type="text/javascript"></script>
</head>

<body>
<div id="main_container">
	<form action="upload.php" method="post" enctype="multipart/form-data">
	
		<input id="uploader" name="userfile" type="file" />
		
		<br /><br />
		
		<input type="submit" value="Upload" id="pxUpload" />
		<input type="reset" value="Clear" id="pxClear" />
	</form>
	<script type="text/javascript">
		$(function(){
			$('#uploader').fileUploader({
				limit: 10,
				imageLoader: 'img/image_upload.gif',
				allowedExtension: 'jpg|jpeg|gif|png|zip',
				callback: function(e) {
					$('#uploaded').append('<input type="text" size="30" value="'+ $(e).contents().find("#uploadedfile").text() +'" /><br />');
				}
			});
		});
	</script>
	<p>Uploaded File Name:</p>
	<div id="uploaded">
		
	</div>
</div>
</body>
</html>