$(document).on("load_app_forum",function(e,hash1,hash2,hash3,hash4){
    $('#content') .html('');
    if(!hash1) $('#content').html('forum under construction!');
    if(hash1 == 'questions')
      display_questions();
    else if(hash1 == 'question')
      display_question(hash2);
    else if(hash1 == 'answer')
      display_answer(hash2);  
});


function question_html(data){
  html = '';
  html += '<div id = "question_'+data.question.id+'">' + data.question.id + '<br>' + data.question.title + '<br>' + data.question.description + '<br><br>' + '</div>';
  return html;
}


function singleanswer_html(data){
  html = '';
  html += data.answer.description + '<br><br>';
  return html;
}

function answer_html(data){
  html = '';
  html += '<a href="#forum/answer/'+data.answer.id+'">Answer </a>' +  data.answer.description + '<br><br>';
  return html;
}



function questions_html(data,i){
  html = '';
  html += '<div id = "question_'+data.questions[i].id+'">' + '<a href="#forum/question/'+data.questions[i].id+'">Question ' + data.questions[i].id + '</a>' + '<br>' + data.questions[i].title + '<br>' + data.questions[i].description + '<br><br>' + '</div>';
  return html;
}


function answers_html(data,i){
  html = '';
  html += '<div id = "answer_'+data.question.id+'">' + data.answers[i].description + '<br><br>' + '</div>';
  return html;
}

function allanswers_html(data){
  html = '';
  html += '<div id = "answers_'+data.question.id+'">';
  for(i=0;i<data.answers.length;i++)
  {
    html += '<a href="#forum/answer/'+data.answers[i].id+'">Answer </a>';
    html += data.answers[i].description + '<br>';
  }
  html += '</div>';
  return html;
}

function display_question(id){
  $.get('forum/fetch_question/',
    {
      'question_id': id
    },function(data)
    {
      html = ''; 
      html += question_html(data);
      html += '<div id="answer_form"><form action="" method="post" onsubmit="add_answer('+data.question.id+');return false;">';
      html += '<input type="text" name="answer">';
      html += '<input type="submit" value="Submit"></div>';
      html += allanswers_html(data);
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
        html += '<button onclick="follow_question('+data.questions[i].id');"> Follow </button>' +  questions_html(data,i);
      }
      $('#content').append(html);
    });
}


function add_answer(question_id){
  $.post('forum/add_answer/',
    {
      'question_id': question_id,
      'description': $('input[name=answer]').val(),
    },function(data)
    {  
      $('#answers_'+question_id).prepend(answer_html(data));
    });
  return false;
}


function display_answer(answer_id){
  $.get('forum/fetch_answer/',
    {
      'answer_id': answer_id
    },function(data)
    {
      html =singleanswer_html(data);
      $('#content').append(html);
    });
}

function follow_question(question_id){
  $.get('forum/follow_question/',
    {
      'question_id': question_id
    },function(data)
