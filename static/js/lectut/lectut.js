var Departments = ["All", "Alternative Hydro Energy Centre", "Architecture and Planning", "Biotechnology", "Chemical", "Civil", "Chemistry", "Earth Science", "Earthquake", "Electrical", "Electronics and Computer Science", "Hydrology", "Humanities", "DPT", "Management Studies", "Mechanical and Indstrial", "Metallurgy", "Physics", "Water Resources Development and Management", "Institute Computer Centre"];

/*var script = document.createElement('script');
script.src = 'jquery.form.js';
script.type = 'text/javascript';
document.getElementsByTagName('script')[0].parentNode.appendChild(script);
*/

function uploadFile(batch_id)
{
  var batch = batch_id;
  if(FileForm==NULL && textForm==NULL)
  {
    alert("Add a file or announcement before submiting");
    return false;
  }
  else if(textForm==NULL)
  {
    if(uploadName==NULL)
    {
      alert("Add name of file");
    }
  }
  else{
  $.ajax({
         type: 'POST',
         url:  'lectut/disp/'+batch_id,
         success:function(data)
         {alert(data);
           alert(data);
         },
      });
  }
}

/*$(document).ready(function() {
$('#uploadFile').ajaxForm(function() {
    alert("Is it really done");
    console.log('dgvtdgv');
    });
    });
*/
var selFile="";
document.addEventListener("DOMContentLoaded", init, false);
function init() {
  document.querySelector('#files').addEventListener('change', handleFileSelect, false);
  selFile = document.querySelector("#selectedFiles");
}

function handleFileSelect(e) {
  if(!e.target.files) return;
  selFile.innerHTML = "";
  var files = e.target.files;
  for(var i=0; i<files.length; i++) {
    var f = files[i];
    selFile.innerHTML += f.name + "<input type='text' id='file_"+i+"'placeholder='description'><br/>";
  }
}

//$("#uploadFile").submit(function(event) {
//$("#post").onclick=function(){
function uploadPost(){
  var $form = $(this);
  formText =  $form.serialize();
  formText = document.getElementById("content").value;
  formData = new FormData();
  formFiles = document.getElementById("files");
  var len=(formFiles.files).length;
  var i;
  for( i=0;i<len;i++)
  {
    fileDescription = document.getElementById("file_"+i).value;
    FileField = JSON.stringify({'description':fileDescription});
    formData.append("upload", formFiles.files[i]);
    formData.append("extra",FileField);
    //formData.append("upload",FileField);
  }
  formData.append('formText', formText);
  formData.append('csrfmiddlewaretoken', csrf_token);
  var batch_id = $('#batch_id').text();
  $.ajax({
       type: 'POST',
       url: '/lectut/ajax/1/upload/',
       enctype: "multipart/form-data",
       data: formData,
       cache: false,
       contentType: false,
       processData: false,
       success:function(data){
       alert(batch_id+"success reached");
       document.getElementById('content').value='';
       selFile.innerHTML = '';
       //document.getElementById('errorMsg').innerHTML=data;
       if(data)
       {
         document.getElementById('errorMsg').innerHTML=data;
       }
       },
       error:function(data){
         //alert('Something went wrong');
         console.log('sdgvzdbdt');
         },
         });
  }
