$(document).on("load_app_forum",function(e,hash1,hash2,hash3,hash4){
    $('#content') .html('');
    if(!hash1) $('#content').html('forum under construction!');
    if(hash1 == 'questions')
        display_questions();
    else if(hash1 == 'question')
        display_question(hash2);
    
});

function display_question(id){
  $.get('forum/fetch_question/',
    {
      'question_id': id
    },function(data)
    { 
      html = '';
      html += data.question.title + '<br>' + data.question.description + '<br><br>'
      for(i=0;i<data.answers.length;i++)
      {
        html += data.answers[i].description + '<br>';
      }
      html += '<form action="" method="post">'
          // + "<input type='hidden' name='csrfmiddlewaretoken' value='{{ csrf_token }}' />";
      html += '<input type="text" name="answer">';
      html += '<input type="submit" value="Submit" onclick="add_answer('+data.question.id+')">';
      $('#content').append(html);
    });
}

function display_questions(){
  $.get('forum/fetch_questions/',
    {
    },function(data)
    {
      html = '';
      for(var i=0;i<data.questions.length;i++)
      {
         html += 'question: ' + data.questions[i].id + '<br>' + data.questions[i].title + '<br>' + data.questions[i].description + '<br><br>';
      }
      $('#content').append(html);
    });
}

function add_answer(question_id){
  $.post('forum/add_answer/',
    {
      'question_id': question_id,
      'description': $('input[name=answer]').val(),
      //'csrfmiddlewaretoken': '{{csrf_token}}'
    },function(data)
    {  
      html = '';
      html += data.question.title + '<br>' + data.question.description + '<br><br>'
      for(i=0;i<data.answers.length;i++)
      {
        html += data.answers[i].description + '<br>';
      }
      html += '<form action="" method="post">';
      html += '<input type="text" name="answer">';
      html += '<input type="submit" value="Submit" onclick="add_answer('+data.question.question_id+')">';
      $('#content').append(html);
    });
}
