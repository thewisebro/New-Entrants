$(document).ready(function(){
  /* Form validation */
  var formSubmitted=false;
  $('form').submit(function(){
    var unfilled = new Array();
    var a=0;
    if($('textarea').length>0){
      var len=$('textarea').val().length;
      if(len>300){
       alert('Please enter your description within 300 characters.');
       return false;
      }
    }
    formSubmitted=false;
    $('form').find('input').each(function(){
      var name=$(this).attr('name');
      if(name=='nonacademic_designation' &&  $('#category').val()!=='nonacademic'){
        return;
      }
      if($(this).attr('type')=='radio'){  
        var str="input[name="+name+"]:checked";
        var value=$(str).val();
        if(value=='' || typeof(value)=='undefined'){
          a=1;
          unfilled.push(name);
          return;
        }
      }
      else{
        value=$(this).val();  
        if(value=='' || typeof(value)=='undefined'){
          a=1;
          unfilled.push(name);
          return;
        }
      }
    });           
    if(a==1){
      var len=unfilled.length;
      
      $('td').css("background-color","#f9f9f9");
      $('.waste_td').css("background-color","rgb(247,240,240)"); 
      for(var i=0;i<len;i++){
        var string=unfilled[i];
        if(string[0]=='D'){
          var str='.'+unfilled[i];
          $(str).css("background-color","#F2DEDE");
          str='#'+string.slice(0,5)+'_ENERGY';
          $(str).css("background-color","#F2DEDE");
        }
        else{  
          var str='#'+unfilled[i];
          $(str).css("background-color","#F2DEDE");
        }
      }
      alert('Please fill the form completely');
      return false;
    }
    else{
     //set formSubmitted to true here when we don't want onbeforeunload to act on Next or Submit
      formSubmitted=false;
    }
  });
  
  /* Ajax Call before the page is closed */
  window.onbeforeunload=window.onunload=function(){
    if(formSubmitted){
      return null;
    }
    $.ajax({
        url:'ajax.php',
        type:'post',
        async:false,
        data:$('textarea').serialize(),
        success:function(data){
        } 
      });   
    //return "The form hasn't been submitted.";
  };
  
  /*Ajax call when input is changed*/
  $('input[type=radio]').change(function(){
    var name=$(this).attr('name');
    var value=$(this).val();
    var str='name='+name+'&value='+value+'&ajax_submit=true';   
    $.ajax({
      url:'ajax_change.php',
      type:'post',
      async:false,
      data:str,
      success:function(data){
      } 
    });         
  });
}); 
