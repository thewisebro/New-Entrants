var Departments = ["All", "Alternative Hydro Energy Centre", "Architecture and Planning", "Biotechnology", "Chemical", "Civil", "Chemistry", "Earth Science", "Earthquake", "Electrical", "Electronics and Computer Science", "Hydrology", "Humanities", "DPT", "Management Studies", "Mechanical and Indstrial", "Metallurgy", "Physics", "Water Resources Development and Management", "Institute Computer Centre"];

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
         {
           alert(data);
         },
      });
  }
}

$("#uploadFile").submit(function(event) {
  var $form = $(this);
  formData =  $form.serialize();
  var batch_id = document.getElementById("batch_id");
  $.ajax({
       type: 'POST',
       url: 'lectut/disp/uploadFile/'+batch_id,

       success:function(data){
       },
       error:function(data){
         alert(data);
         },
         });
  });  
