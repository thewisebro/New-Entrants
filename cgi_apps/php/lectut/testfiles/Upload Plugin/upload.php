<?php
include("classes/easy_upload/upload_class.php"); //classes is the map where the class file is stored

$max_size = 10*10; // the max. size for uploading
$_POST['MAX_FILE_SIZE'] = $max_size;

$upload = new file_upload();

$upload->upload_dir = 'uploads/';
$upload->extensions = array('.png', '.jpg', '.zip', '.pdf'); // specify the allowed extensions here
$upload->rename_file = true;


if(!empty($_FILES)) {
	$upload->the_temp_file = $_FILES['userfile']['tmp_name'];
	$upload->the_file = $_FILES['userfile']['name'];
	$upload->http_error = $_FILES['userfile']['error'];
	$upload->do_filename_check = 'y'; // use this boolean to check for a valid filename
	if ($upload->upload()){
		echo '<div id="output">success</div>';
		echo '<div id="message">'. $upload->file_copy .' Uploaded</div>';
		//return the upload file
		echo '<div id="uploadedfile">'. $upload->file_copy .'</div>';
	} else {
		echo '<div id="output">failed</div>';
		echo '<div id="message">'. $upload->show_error_string() .'</div>';
	}
	echo $upload->file_copy;
}
?>
