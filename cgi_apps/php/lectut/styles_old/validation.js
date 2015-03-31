function validate_required(text,alerttxt)
{
with(text)
 {
 if(value=="")
  {
   alert(alerttxt);return false
  }
  else
  {
    return true
  }
 }
}
function validate_form(text1,text2,text3,thisform)
{

with(thisform)
{
with(text1)
 {

   if(validate_required(text1,"Please enter the subject code")==false)
  {
   text1.focus();return false
  }
 }
with(text2)
{
   if(validate_required(text2,"Please enter the title")==false)
    {
      text2.focus();return false
    }
}
with(text3)
{
  if(validate_required(text3,"Please select file you want to upload")==false)
  {
   text3.focus();return false
  }
}
}
}
