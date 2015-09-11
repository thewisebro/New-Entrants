$(document).ready(function() {
    $('select').filter(
      function(){
        return this.id.match(/id_options/) && this.value != 'NOT' && this.value != '4P Education' && this.value != 'Ethuns Consultancy Service';
      }).parent().next().hide();


    options = $('#id_options')
    if (options.val() == '4P Education') {
      options.parent().next().show();
      options.parent().next().children().get(0).innerHTML='Fill at least one topic from given options';
      options.parent().next().children().get(1).setAttribute('placeholder','Case Study, HR interview, Personal Interview, Group Discussion');
      options.parent().next().children().get(2).innerHTML='Case Study, HR interview, Personal Interview, Group Discussion';
    }
    else if (options.val() == 'Ethuns Consultancy Service') {
      options.parent().next().show();
      options.parent().next().children().get(0).innerHTML='Fill the sector for mock interview';
      options.parent().next().children().get(1).setAttribute('placeholder','');
      options.parent().next().children().get(2).innerHTML='IT/Software, Electronics/Electrical, Mechanical, Chemical, Civil, Finance/Consulting etc.';
    }

    $('select').filter(function(){return this.id.match(/id_options/)}).change(function(){
        if(this.value == 'NOT')
          $(this).parent().next().show();
        else if(this.value == '4P Education'){
          $(this).parent().next().show();
          $(this).parent().next().children().get(0).innerHTML='Fill at least one topic from given options';
          $(this).parent().next().children().get(1).setAttribute('placeholder','Case Study/HR interview/Personal Interview/Group Discussion');
          $(this).parent().next().children().get(2).innerHTML='Case Study, HR interview, Personal Interview, Group Discussion';
        }
        else if(this.value == 'Ethuns Consultancy Service'){
          $(this).parent().next().show();
          $(this).parent().next().children().get(0).innerHTML='Fill the sector for mock interview';
          $(this).parent().next().children().get(1).setAttribute('placeholder','');
          $(this).parent().next().children().get(2).innerHTML='IT/Software, Electronics/Electrical, Mechanical, Chemical, Civil, Finance/Consulting etc.';
        }
        else
          $(this).parent().next().hide();
      });
});


