$(document).on("load_app_forum",function(e,hash1,hash2,hash3,hash4){
    $('#content') .html('');
    if(!hash1) $('#content').html('forum under construction!');
    if(hash1 == 'questions')
      display_questions();
    else if(hash1 == 'question')
      display_question(hash2);
    else if(hash1 == 'answer')
      display_answer(hash2);
    else if(hash1 == 'tag')
      display_tag(hash2);
    else if(hash1 == 'activity')
      display_activity();
});


function escapeStr(str) 
{
      if (str)
                return str.replace(/([ #;?%&,.+*~\':"!^$[\]()=>|\/@])/g,'\\$1');      

                      return str;
}


function question_html(data){
  html = '';
  html += '<div id = "question_'+data.question.id+'">' + data.question.id + '<br>' + data.question.title + '<br>' + data.question.description + '<br><br>';
  if(data.question.follow_unfollow=="true")
    html += '<div id = "follow_unfollow_'+data.question.id+'"><button onclick="unfollow_question('+data.question.id+')">Unfollow</button></div>';
  else
    html += '<div id = "follow_unfollow_'+data.question.id+'"><button onclick="follow_question('+data.question.id+')">Follow</button></div>';
  for(i=0;i<data.tags.length;i++)
  {
    html += '<div id = "tag_'+data.tags[i].name+'"><a href="#forum/tag/'+data.tags[i].name+'">' + data.tags[i].name + '</a></div>';
  } 
  html += '<br><br></div>';
  return html;
}


function singleanswer_html(data){
  html = '';
  html += question_html(data);
  html += data.answer.description + '<br><br>';
  if(data.answer.same_profile=="false")
  {
    if(data.answer.upvote=="true")
    {
      html += '<div id = "upvote_'+data.answer.id+'"><button onclick="remove_upvote('+data.answer.id+')">Upvoted</button></div>';
      html += '<div id = "count_'+data.answer.id+'">' + data.answer.upvote_count + '</div>';
      html += '<div id = "downvote_'+data.answer.id+'"><button onclick="downvote_answer('+data.answer.id+')">Downvote</button></div>';
    }
    else if(data.answer.downvote=="true")
    {
      html += '<div id = "upvote_'+data.answer.id+'"><button onclick="upvote_answer('+data.answer.id+')">Upvote</button></div>';
      html += '<div id = "count_'+data.answer.id+'">' + data.answer.upvote_count + '</div>';
      html += '<div id = "downvote_'+data.answer.id+'"><button onclick="remove_downvote('+data.answer.id+')">Downvoted</button></div>';
    }
    else
    {
      html += '<div id = "upvote_'+data.answer.id+'"><button onclick="upvote_answer('+data.answer.id+')">Upvote</button></div>';
      html += '<div id = "count_'+data.answer.id+'">' + data.answer.upvote_count + '</div>';
      html += '<div id = "downvote_'+data.answer.id+'"><button onclick="downvote_answer('+data.answer.id+')">Downvote</button></div>';
    } 
  }
  else
  {
    if(data.answer.upvote=="true")
    {
      html += '<div id = "upvote_'+data.answer.id+'"><button>Upvoted</button></div>';
      html += '<div id = "count_'+data.answer.id+'">' + data.answer.upvote_count + '</div>';
      html += '<div id = "downvote_'+data.answer.id+'"><button>Downvote</button></div>';
    }
    else if(data.answer.downvote=="true")
    {
      html += '<div id = "upvote_'+data.answer.id+'"><button>Upvote</button></div>';
      html += '<div id = "count_'+data.answer.id+'">' + data.answer.upvote_count + '</div>';
      html += '<div id = "downvote_'+data.answer.id+'"><button>Downvoted</button></div>';
    }
    else
    {
      html += '<div id = "upvote_'+data.answer.id+'"><button>Upvote</button></div>';
      html += '<div id = "count_'+data.answer.id+'">' + data.answer.upvote_count + '</div>';
      html += '<div id = "downvote_'+data.answer.id+'"><button>Downvote</button></div>';
    } 
  }
  return html;
}

function answer_html(data){
  html = '';
  html += '<a href="#forum/answer/'+data.answer.id+'">Answer </a>' +  data.answer.description + '<br><br>';
  return html;
}



function questions_html(data,i){
  html = '';
  html += '<div id = "question_'+data.questions[i].id+'">' + '<a href="#forum/question/'+data.questions[i].id+'">Question ' + data.questions[i].id + '</a>' + '<br>' + data.questions[i].title + '<br>' + data.questions[i].description + '<br>';
  if(data.questions[i].follow_unfollow=="true")
    html += '<div id = "follow_unfollow_'+data.questions[i].id+'"><button onclick="unfollow_question('+data.questions[i].id+')">Unfollow</button></div>';
  else
    html += '<div id = "follow_unfollow_'+data.questions[i].id+'"><button onclick="follow_question('+data.questions[i].id+')">Follow</button></div>';
  html += '<br><br></div>';
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

function activities_html(data,i){
  html = '';
  html += '<div id = "activity_'+i+'">';
  html += data.activities[i].student_name;
  if(data.activities[i].activity_type=='ASK_QUES')
  {
    html += ' asked a ' + '<a href="#forum/question/'+data.activities[i].object_id+'">question</a>'
  }
  else if(data.activities[i].activity_type=='POST_ANS')
  {
    html += ' posted an ' + '<a href="#forum/answer/'+data.activities[i].object_id+'">answer</a>' + 'to a question';
  }
  else if(data.activities[i].activity_type=='FOL_QUES')
  {
    html += ' followed a ' + '<a href="#forum/question/'+data.activities[i].object.id+'">question</a>';
  }
  else if(data.activities[i].activity_type=='UP_ANS')
  {
    html += ' upvoted an ' + '<a href="#forum/answer/'+data.activities[i].object.id+'">answer</a>';
  }
  else if(data.activities[i].activity_type=='FOL_TOPIC')
  {
    html += ' followed a ' + '<a href="#forum/tag/'+data.activities[i].object.name+'">tag</a>';
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
      if (data.question.same_profile=="false")
      {
        html += '<div id="answer_form"><form action="" method="post" onsubmit="add_answer('+data.question.id+');return false;">';
        html += '<input type="text" name="answer">';
        html += '<input type="submit" value="Submit"></div>';
      }
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
      for(var i=data.questions.length;i>0;i--)
      {
        html +=  questions_html(data,i-1);
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
      $('input[name=answer]').val('');
    });
  return false;
}


function display_answer(answer_id){
  $.get('forum/fetch_answer/',
    {
      'answer_id': answer_id
    },function(data)
    {
      html = singleanswer_html(data);
      $('#content').append(html);
    });
}

function follow_question(question_id){
  $.get('forum/follow_question/',
    {
      'question_id': question_id
    },function(data)
    {
      html =  '<button onclick="unfollow_question('+question_id+');"> Unfollow </button>';
      $('#follow_unfollow_'+question_id).html(html);
    });
}

function unfollow_question(question_id){
  $.get('forum/unfollow_question/',
    {
      'question_id': question_id
    },function(data)
    {
      html =  '<button onclick="follow_question('+question_id+');"> Follow </button>';
      $('#follow_unfollow_'+question_id).html(html);
    });
}

function remove_upvote(answer_id){
  $.get('forum/remove_upvote/',
    {
      'answer_id': answer_id
    },function(data)
    {
      html = '<button onclick="upvote_answer('+answer_id+')">Upvote</button>';
      $('#upvote_'+answer_id).html(html);
      html = data.count;
      $('#count_'+answer_id).html(html);

    });
}

function remove_downvote(answer_id){
  $.get('forum/remove_downvote/',
    {
      'answer_id': answer_id
    },function(data)
    {
      html = '<button onclick="downvote_answer('+answer_id+')">Downvote</button>';
      $('#downvote_'+answer_id).html(html);
    });
}

function upvote_answer(answer_id){
  $.get('forum/upvote_answer/',
    {
      'answer_id': answer_id
    },function(data)
    {
      html = '<button onclick="remove_upvote('+answer_id+')">Upvoted</button>';
      $('#upvote_'+answer_id).html(html);
      html = data.count;
      $('#count_'+answer_id).html(html);
      html = '<button onclick="downvote_answer('+answer_id+')">Downvote</button>';
      $('#downvote_'+answer_id).html(html);
    });
}

function downvote_answer(answer_id){
  $.get('forum/downvote_answer/',
    {
      'answer_id': answer_id
    },function(data)
    {
      html = '<button onclick="remove_downvote('+answer_id+')">Downvoted</button>';
      $('#downvote_'+answer_id).html(html);
      html = data.count;
      $('#count_'+answer_id).html(html);
      html = '<button onclick="upvote_answer('+answer_id+')">Upvote</button>';
      $('#upvote_'+answer_id).html(html);
    });
}

function display_tag(tag_name){
  $.get('forum/fetch_tag/',
    {
      'tag_name': tag_name
    },function(data)
    {
      html = '';
      if(data.tag.follow_unfollow=="true")
        html += '<div id="follow_unfollow_tag_'+tag_name+'"><button onclick=\"unfollow_tag(\''+tag_name+'\')\"> Unfollow </button></div>';
      else
        html += '<div id="follow_unfollow_tag_'+tag_name+'"><button onclick=\"follow_tag(\''+tag_name+'\')\"> Follow </button></div>';
      for(var i=data.questions.length;i>0;i--)
      {
        html +=  questions_html(data,i-1);
      }
      $('#content').append(html);
    });
}

function display_activity(){
  $.get('forum/fetch_activity/',
    {
    },function(data)
    {
      html = '';
      for(i=data.activities.length;i>0;i--)
      {
        html += activities_html(data,i-1);
      }
      $('#content').html(html);
    });
}

function follow_tag(tag_name){
  $.get('forum/follow_tag/',
    {
      'tag_name': tag_name
    },function(data)
    {
      html =  '<button onclick=\"unfollow_tag(\''+tag_name+'\')\"> Unfollow </button>';
      $('#follow_unfollow_tag_'+escapeStr(tag_name)).html(html);
    });
}

function unfollow_tag(tag_name){
  $.get('forum/unfollow_tag/',
    {
      'tag_name': tag_name
    },function(data)
    {
      html =  '<button onclick=\"follow_tag(\''+tag_name+'\')\"> Follow </button>';
      $('#follow_unfollow_tag_'+escapeStr(tag_name)).html(html);
    });
}

