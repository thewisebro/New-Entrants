<?
error_reporting(0);

?>

<form  action="uploadPicPost.php" method="post" enctype="multipart/form-data">

   <input type="hidden" name="MAX_FILE_SIZE" value="10000000000" />
   <input type="hidden" name="username" value="<?echo $username?>" />
   <input type="hidden" name="sessionid" value="<?echo $sessionid?>" />
  Choose an image to Upload:<br />
   <input name="userfile" type="file" size="35"/>
   <br />
    Description:<br />
   <textarea rows="3" cols="40" name="description"> </textarea>
  <input type="submit" value="Upload Image" />
</table>
</form>




<?


$filename=$_FILES['userfile']['name'];
$filelocation=$_FILES['userfile']['tmp_name'];
$filesize=$_FILES['userfile']['size'];
$filetype = substr($filename, strrpos($filename, ".")+1);
$filename = substr($filename, 0, strrpos($filename, "."));
$description = $_POST['description'];

		$special=array("`","~","!","@","#","$","%","^","&","*","(",")","_","=","+","\\","|","]","}","[","{","'","\"",";",":","/","?",".",">",",","<");
		$filename=str_replace($special,"",$filename);
		$description=str_replace($special,"",$description);
		
				ob_start();
                                $type=system("file -i -b $filelocation");
                                ob_end_clean();

                                $pos=strpos($type, ";");
                                if($pos)
                                        {
                                        $type=substr($type, 0, $pos);
                                        }

                                $pos1=strpos($type,",");
                                if($pos1)
                                        {
                                        $type=substr($type, 0,$pos1);
                                        }


if(isset($filename,$filesize) && ( $filetype =="gif"  || $filetype=="jpeg" || $filetype=="jpg"  || $filetype=="png" ) && (is_uploaded_file($filelocation)))  {

                if(  $type=="image/gif"  || $type=="image/jpeg" || $type=="image/png" )
                               {
		
			$rand=rand();
                        $filename_generated=$filename.$rand.'.'.$filetype;


		$query="INSERT INTO uploaded_images (username,name) VALUES ('$username''$filename$rand')";
		$result = pg_query($dbcon,$query);
		
		if($result)
		{
			rename($filename.'.'.$filetype  , $filename_generated );
			move_uploaded_file($filelocation,$root_dir_iitrgallery.'/'.$filename_generated);
			echo "<br>File $filename uploaded</br>";
		}                
		
		}
		else 
			{
			echo "Invalid File Type";
			}
		}
                else 
			{
                	echo "Invalid File Type";
                	}


pg_close($dbcon);


?>

