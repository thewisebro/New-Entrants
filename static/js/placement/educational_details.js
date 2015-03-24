$(document).ready(function() {
    // Assumes that discipline provided is the first field after discipline
    // Hide discipline provided if disciplines value is not 'None Of These'
    $('select').filter(function(){return this.id.match(/id_form-\d+-discipline/) && this.value != 'NOT';}).parent().next().hide();
    // Check whether to show/hide discipline provided everytime the value of discipline is changed
    $('select').filter(function(){return this.id.match(/id_form-\d+-discipline/)}).change(function(){
        if(this.value == 'NOT')
          $(this).parent().next().show();
        else
          $(this).parent().next().hide();
      });
});

