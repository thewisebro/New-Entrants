i<?php
$MAXIMUM_FILESIZE = 1024 * 200 * 100000; // 200KB
$MAXIMUM_FILE_COUNT = 10; // keep maximum 10 files on server
echo exif_imagetype($_FILES['Filedata']);
if ($_FILES['Filedata']['size'] <= $MAXIMUM_FILESIZE)
{
    move_uploaded_file($_FILES['Filedata']['tmp_name'], "./uploads/".$_FILES['Filedata']['name']);
 
}
														    ?>
