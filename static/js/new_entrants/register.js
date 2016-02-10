$('#registration').submit(function(e){
  e.preventDefault();
  $.ajax({
    url:'/new_entrants/register/',
    type:'POST',
    dataType:'json',
    data: $('#registration').serialize(),
    success: function(data){
      console.log(data);
    },
    error: function(errorThrown){
      console.log(errorThrown);
    }
  });
});
