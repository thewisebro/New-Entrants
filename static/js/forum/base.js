var current_state = null;
var right_visible = true;
function yes_category(){
  var html =        '<div id="forum-category">' +
                  '<div id="category-box">' +
                    '<a class="category-link" href="#forum/">' +
                      '<div id="all" class="category">' +
                        'All' +
                      '</div>' + //category
                    '</a>' +
                    '<a class="category-link" href="#forum/unanswered/">' +
                      '<div id="unanswered" class="category">' +
                        'Unanswered' +
                      '</div>' + //category
                    '</a>' +
                    '<a class="category-link" href="#forum/mytopic/">' +
                      '<div id="mytopic" class="category">' +
                        'My Topic' +
                      '</div>' + //category
                    '</a>' +
                    '<a class="category-link" href="#forum/popular/">' +
                      '<div id="popular" class="category">' +
                        'Popular' +
                      '</div>' + //category
                    '</a>' +
                  '</div>' + //category-box
                  '<div id="add-question-div">' +
                    '<div class="div-button" onclick="ask_question();">Ask Question</div>' +
                  '</div>' + //add-question-div
                '</div>'; //forum-category
  return html;
}

$(document).on("unload_app_forum",function(){
   right_visible = false;
   });
$(document).on("load_app_forum",function(e,hash1,hash2,hash3,hash4){
    if(!user.is_authenticated){
      nucleus.redirect_to_home();
      return;
    }
    //html = '';
    //html += '<div id="tag_search"><form action="" method="post" onsubmit="search_tag();return false;">';
    //html += '<input type="text" name="tag_key">';
    //html += '<input type="submit" value="Search"></div>';
    $('#content').html('');
    var next_state = null;
    if(!hash1)
    {
      next_state = 'yes_category';
    }
    else if(hash1 == 'questions')
    {}
    else if(hash1 == 'question')
    {}
    else if(hash1 == 'answer')
    {}
    else if(hash1 == 'tag')
    {}
    else if(hash1 == 'activity')
    {
      if(!hash2)
      {}
      else
      {}
    }
    else if(hash1 == 'unanswered')
    {
      next_state = 'yes_category';
    }
    else if(hash1 == 'mytopic')
    {
      next_state = 'yes_category';
    }
    else if(hash1 == 'popular')
    {
      next_state = 'yes_category';
    }
    if((next_state != current_state) || (right_visible === false))
    {
      right_visible = true;
      current_state = next_state;
      var html = '';
      if(current_state == 'yes_category')
      {
        html = yes_category();
      }
      $('#right-column .content').html(html);
    }
    if(!hash1)
    {
      display_activity(0,0);
    }
    else if(hash1 == 'questions')
      display_questions();
    else if(hash1 == 'question')
      display_question(hash2);
    else if(hash1 == 'answer')
      display_answer(hash2);
    else if(hash1 == 'tag')
      display_tag(hash2);
    else if(hash1 == 'activity')
    {
      if(!hash2)
        display_activity(1,0);
      else
        display_activity(1,hash2);
    }
    else if(hash1 == 'unanswered')
    {
      display_category(1);
    }
    else if(hash1 == 'mytopic')
    {
      display_category(2);
    }
    else if(hash1 == 'popular')
    {
      display_category(3);
    }
});

function escapeStr(str)
{
      if (str)
                return str.replace(/([ #;?%&,.+*~\':"!^$[\]()=>|\/@])/g,'\\$1');

                      return str;
}


function question_html(data){
  var html = '';
  html += '<div class="feed-box">' +
            '<a href="#"><img class="feed-propic" src="'+data.question.photo_url+'"></a>' +
              '<div class="feed-text">';
  html += '<div class="feed-line">' +
            '<a class="person-name" href="#">' + data.question.user_name + '</a>' +
            '<span>\'s question </span>' +
          '</div>'; //feed-line


  html += '<div class="feed-description">' +
            '<div class="question-page-title">' +
              data.question.title + 
            '</div>' + 
            '<div class="question-page-description">' +
              data.question.description +
            '</div>';
  html += '<div class="tags">';
  for(i=0;i<data.tags.length;i++)
  {
    html += '<a href="#forum/tag/'+data.tags[i].name+'">' + '<div class="question-tag">' +data.tags[i].name + '</div>' + '</a>' + '  ';
  }
  html += '<div class="clear"></div>';
  html += '</div>'; // tags
  if(data.question.follow_unfollow=="true")
    html += '<div id = "follow_unfollow_'+data.question.id+'" style="float:left">' + 
              '<div class="follow-question-button">' +
                '<button class="grey-button" onclick="unfollow_question('+data.question.id+','+data.question.num_followers+')">Followed</button>' + 
              '</div>' + //follow-question-button
            '<div class="clear"></div>' +
            '</div>';
  else
    html += '<div id = "follow_unfollow_'+data.question.id+'" style="float:left">' + 
              '<div class="follow-question-button">' +
                '<button class="blue-button" onclick="follow_question('+data.question.id+','+data.question.num_followers+')">Follow Question</button>' + 
              '</div>' + //follow-question-button
            '<div class="clear"></div>' +
            '</div>';
  if(data.question.num_followers < 1)
    html += '<div class="followers-number">' + '<div id="followers_number_'+data.question.id+'" style="float:left;margin-right:2px">' + '</div>' + '<div id="followers_word" style="float:left">' + '</div>' + '</div>';
  if(data.question.num_followers == 1)
    html += '<div class="followers-number">' + '<div id="followers_number_'+data.question.id+'" style="float:left;margin-right:2px">' + data.question.num_followers + '</div>' + '<div id="followers_word" style="float:left">' + ' Follower' + '</div>' + '</div>';
  if(data.question.num_followers > 1)
    html += '<div class="followers-number">' + '<div id="followers_number_'+data.question.id+'" style="float:left;margin-right:2px">' + data.question.num_followers + '</div>' + '<div id="followers_word" style="float:left">' + ' Followers' + '</div>' + '</div>';
  html += '<div class="clear"></div>';
  html += '</div>'; //feed-description
  html += '</div>'; //feed-text
  html += '</div>'; //feed-box
  html += '<div class="hr"></div>';
  //html += '</div>';
  return html;
}


function singleanswer_html(data){
  var html = '';
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
  html += '<div id = "answer_comments_'+data.answer.id+'"></div>';
  return html;
}

function answer_html(data){
  html = '<div class="feed-box">' +
           '<a href="#"><img class="feed-propic" src="'+data.answer.photo_url+'"></a>' +
             '<div class="feed-text">' +
               '<div class="feed-line">' + 
                 '<span>' + '<a class="person-name" href="#">' + 
                   data.answer.user_name +
                 '</a>' + '</span>' +
                                                                                                                                //'<div class="clear"></div>' +
               '</div>'; //feed-line

  html += '<div class="feed-description">';
         // html += '<a href="#forum/answer/'+data.answers[i].id+'">Answer </a>';
  html += data.answer.description;
  html += '</div>'; //feed-description
  html += '<div class="feed-bottom-line">'; 
  html += '<div id="comments_'+data.answer.id+'">';
  html += '<div id="show_hide_comments_'+data.answer.id+'" onclick="show_comments('+data.answer.id+')"> Show comments </div>';
  html += '<div id="answer_comments_'+data.answer.id+'"></div>';
  html += '</div>'; //comments_
  html += '</div>'; //feed-bottom-line
  html += '</div>'; //feed-text
  html += '</div>'; //feed-box
  return html;
}



function questions1_html(data,i){
  var html = '';
  html += '<div id = "question_'+data.questions[i].id+'">' + '<a href="#forum/question/'+data.questions[i].id+'">Question ' + data.questions[i].id + '</a>' + '<br>' + data.questions[i].title + '<br>' + data.questions[i].description + '<br>';
  if(data.questions[i].follow_unfollow=="true")
    html += '<div id = "follow_unfollow_'+data.questions[i].id+'"><button onclick="unfollow_question('+data.questions[i].id+')">Followed</button></div>';
  else
    html += '<div id = "follow_unfollow_'+data.questions[i].id+'"><button onclick="follow_question('+data.questions[i].id+')">Follow Question</button></div>';
  html += '<br><br></div>';
  return html;
}

function questions_html(data,i,type_question){
  var html = '' +
         '<div class="feed-box">' +
          '<a herf="#"></a>' +
          '<a href="#"><img class="feed-propic" src="'+data.questions[i].photo_url+'"></a>' +
          '<div class="feed-text">' +
            '<div class="feed-line">' + 
              '<span>' + 
                data.questions[i].user_name + 
              '</span>' +
            '</div>' + //feed-line
            '<div class="feed-description">' + 
              '<div class="feed-question">' +
                '<a class="question-title" href="/#forum/question/'+data.questions[i].id+'">' +
                  data.questions[i].title +
                '</a>' +
                '<div class="question-description">' +
                  data.questions[i].description +
                '</div>' + //question-description
              '</div>' + //feed-question
            '</div>' + //feed description
            '<div class="feed-bottom-line">' +
              '<a class="answers-number" href="/#forum/question/'+data.questions[i].id+'">';
  if(type_question==1)
    html += 'Be the first one to answer';
  else
  {
    html += data.questions[i].answers_number;
    if(data.questions[i].answers_number <= 1)
      html += ' Answer';
    else
      html += ' Answers';
  }
  html +=       '</a>' +
              '</div>' + //feed-bottom-line
            '</div>' + //feed-texit
          '</div>'; //feed-box
  return html;
}

function answers_html(data,i){
  var html = '';
  html += '<div id = "answer_'+data.question.id+'">' + data.answers[i].description + '<br><br>' + '</div>';
  return html;
}

function allanswers_html(data){
  var html = '';
  html += '<div id = "answers_'+data.question.id+'">';
  for(i=0;i<data.answers.length;i++)
  {
    html += '<div class="feed-box">' +
              '<a href="#"><img class="feed-propic" src="'+data.answers[i].photo_url+'"></a>' +
               '<div class="feed-text">' +
                 '<div class="feed-line">' + 
                   '<span>' + '<a class="person-name" href="#">' + 
                     data.answers[i].user_name +
                   '</a>' + '</span>' +
                   //'<div class="clear"></div>' +
                 '</div>'; //feed-line

    html += '<div class="feed-description">';
   // html += '<a href="#forum/answer/'+data.answers[i].id+'">Answer </a>';
    html += data.answers[i].description;
    html += '</div>'; //feed-description
    html += '<div class="feed-bottom-line">'; 
    html += '<div id="comments_'+data.answers[i].id+'">';
    html += '<div id="show_hide_comments_'+data.answers[i].id+'" onclick="show_comments('+data.answers[i].id+')"> Show comments </div>';
    html += '<div id="answer_comments_'+data.answers[i].id+'"></div>';
    html += '</div>'; //comments_
    html += '</div>'; //feed-bottom-line
    html += '</div>'; //feed-text
    html += '</div>'; //feed-box
  }
  html += '</div>';
  return html;
}

function activities_html(data,i){
  var html = '';
  html += '<div class = "feed-box">';
 // html += '<a href="#"></a>';
 // html += data.activities[i].user_name;
  if(data.activities[i].activity_type=='ASK_QUES')
  {
    html += '<a href="#"><img class="feed-propic" src="'+data.activities[i].photo_url+'"></a>' +
            '<div class="feed-text">' +
              '<div class="feed-line">' + 
                '<span>' +
                  data.activities[i].user_name + 
                  ' asked a question' +
                '</span>' +
              '</div>' + //feed-line
              '<div class="feed-description">' + 
                '<a href="/#forum/question/'+data.activities[i].object.id+'">' +
                  '<div class="feed-question">' +
                    '<div class="question-title">' +
                      data.activities[i].object.title +
                    '</div>' +
                    '<div class="question-description">' +
                      data.activities[i].object.description +
                    '</div>' + //question-description
                  '</div>' + //feed-question
                '</a>' + //feed-question
              '</div>' + //feed description
              '<div class="feed-bottom-line">' +
                '<a class="answers-number" href="/#forum/question/'+data.activities[i].object.id+'">' +
                  data.activities[i].object.answers_number;
                  if(data.activities[i].object.answers_number <= 1)
                    html += ' Answer';
                  else
                    html += ' Answers';
       html += '</a>' +
              '</div>' + //feed-bottom-line
            '</div>'; //feed-text

  }
  else if(data.activities[i].activity_type=='POST_ANS')
  {
          html += '<a href="#"><img class="feed-propic" src="'+data.activities[i].photo_url+'"></a>' +
                  '<div class="feed-text">' +
                    '<div class="feed-line">' + 
                      '<span>' + 
                        data.activities[i].user_name + 
                        ' answered a question' +
                      '</span>' +
                    '</div>' + //feed-line
                    '<div class="feed-description">' +
                      '<a href="/#forum/question/'+data.activities[i].object.question_id+'">' +
                      '<div class="feed-answer-box">' +
                        '<div class="question-title-box">' +
                          '<div class="question-title">' +
                            data.activities[i].object.title +
                          '</div>' + //question-title
                        '</div>' + //question-title-box
                        '<div class="answer-line">' +
                          data.activities[i].user_name +
                          '\'s answer:' +
                        '</div>' + //answer-line
                        '<div class="answer-box">' +
                          data.activities[i].object.description +
                        '</div>' + //answer-box
                      '</div>' + //feed-answer-box
                      '</a>' +
                    '</div>' + //feed-description
                  '</div>';//feed-text

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
  html += '</div>'; //feed-box
  return html;
}

function ask_question(){
  /*
  var html = '<div class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-front dialog-class" tabindex="-1" role="dialog" style="position: fixed; height: auto; width: 920px; top: 50px; left: 327px; display: block;" aria-describedby="add_event_dialog-div" aria-labelledby="ui-id-1">' + 
               '<div class="ui-dialog-titlebar ui-widget-header ui-corner-all ui-helper-clearfix">' +
                 '<span id="ui-id-1" class="ui-dialog-title">Ask Question</span>' +
                 '<button class="ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only ui-dialog-titlebar-close" role="button" aria-disabled="false" title="close">' +
                   '<span class="ui-button-icon-primary ui-icon ui-icon-closethick"></span>' +
                   '<span class="ui-button-text">close</span>' +
                 '</button>' +
               '</div>' +
               '<div id="add_event_dialog-div" class="ui-dialog-content ui-widget-content" style="width: auto; min-height: 0px; max-height: none; height: 205px;">' +
                 '<iframe id="add_event_dialog-iframe" src="/forum/ask_question/" width="100%" height="98%" frameborder="0"></iframe>' +
               '</div>' +
             '</div>';
  
  var html = '<div class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-front dialog-class" tabindex="-1" role="dialog" style="position: fixed; height: auto; width: 920px; top: 50px; left: 327px; display: block;" aria-describedby="add_event_dialog-div" aria-labelledby="ui-id-1">' + 
               '<div class="ui-dialog-titlebar ui-widget-header ui-corner-all ui-helper-clearfix">' +
                 '<span id="ui-id-1" class="ui-dialog-title">Ask Question</span>' +
                 '<button class="ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only ui-dialog-titlebar-close" role="button" aria-disabled="false" title="close">' +
                   '<span class="ui-button-icon-primary ui-icon ui-icon-closethick"></span>' +
                   '<span class="ui-button-text">close</span>' +
                 '</button>' +
               '</div>' +
               '<div id="add_event_dialog-div" class="ui-dialog-content ui-widget-content" style="width: auto; min-height: 0px; max-height: none; height: 205px;">' +
                 '<iframe id="add_event_dialog-iframe" src="/forum/ask_question/" width="100%" height="98%" frameborder="0"></iframe>' +
               '</div>' +
             '</div>';
*/
  dialog_iframe({
    name:'forum_ask_question',
    title:'Ask Question',
    width:1000,
    height:450,
    src:'/forum/ask_question/'
  });
}

function display_question(id){
  $.get('forum/fetch_question/',
    {
      'question_id': id
    },function(data)
    {
      var html = '';
      html += question_html(data);
      if (data.question.same_profile=="false")
      {
        html += '<div class="feed-box">' +
                  '<a href="#"><img class="feed-propic" src="'+data.question.viewer_photo+'"></a>';

        html += '<div class="feed-text">';
        html += '<div id="answer_form"><form action="" method="post" onsubmit="add_answer('+data.question.id+');return false;">';
        html += '<textarea name="answer" class="answer-field" placeholder="Add your answer">' + '</textarea>';
        html += '<div class="submit-button">';
        html += '<input type="submit" value="Submit" class="blue-button">';
        html += '</div>'; //submit-button
        html += '</div>'; //answer_form
        html += '<div class="clear"></div>';
        html += '</div>'; //feed-text
        html += '</div>'; //feed-box
        html += '<div class="hr"></div>';
      }
      html += allanswers_html(data);
      $('#content').html(html);
      $('#content').pickify_users();
    });
}


function display_questions(){
  $.get('forum/fetch_questions/',
    {
      'type_question': 0,
    },function(data)
    {
      var html = '';
      for(var i=data.questions.length;i>0;i--)
      {
        html +=  questions_html(data,i-1,0);
      }
      $('#content').append(html);
    });
}


function add_answer(question_id){
  $.post('forum/add_answer/',
    {
      'question_id': question_id,
      'description': $('textarea[name=answer]').val(),
    },function(data)
    {
      $('#answers_'+question_id).prepend(answer_html(data));
      $('textarea[name=answer]').val('');
    });
  return false;
}


function display_answer(answer_id){
  $.get('forum/fetch_answer/',
    {
      'answer_id': answer_id
    },function(data)
    {
      var html = singleanswer_html(data);
      $('#content').append(html);
      $('#answer_comments_'+answer_id).load('forum/answer_comments/'+data.answer.id);
    });
}

function follow_question(question_id,followers_number){
  $.get('forum/follow_question/',
    {
      'question_id': question_id
    },function(data)
    {
      var x = followers_number + 1;
      var html = null;
      if(x == 2)
      {
        html = ' Followers';
        $('#followers_word').html(html);
      }
      if(x == 1)
      {
        html = ' Follower';
        $('#followers_word').html(html);
      }
      followers_number = x;
      html = '' + x +'';
      $('#followers_number_'+question_id).html(html);
      html =  '<div class="follow-button-box">' + 
                '<button class="grey-button" onclick="unfollow_question('+question_id+','+followers_number+');"> Followed </button>' +
              '</div>' + //follow-button-box
              '<div class="clear"></div>';
      $('#follow_unfollow_'+question_id).html(html);
    });
}

function unfollow_question(question_id,followers_number){
  $.get('forum/unfollow_question/',
    {
      'question_id': question_id
    },function(data)
    {
      var x = followers_number - 1;
      var html = null;
      if(followers_number == 2)
      {
        html = ' Follower';
        $('#followers_word').html(html);
      }
      if(followers_number == 1)
      {
        html = '';
        $('#followers_word').html(html);
      }
      followers_number = x;
      if(x === 0)
      {
        html = '';
      }
      else
      {
        html = '' + x +'';
      }
      $('#followers_number_'+question_id).html(html);
      html =  '<div class="follow-button-box">' +
                    '<button class="blue-button" onclick="follow_question('+question_id+','+followers_number+');"> Follow Question </button>' +
                  '</div>' + //follow-button-box
                  '<div class="clear"></div>';
      $('#follow_unfollow_'+question_id).html(html);
    });
}

function remove_upvote(answer_id){
  $.get('forum/remove_upvote/',
    {
      'answer_id': answer_id
    },function(data)
    {
      var html = '<button onclick="upvote_answer('+answer_id+')">Upvote</button>';
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
      var html = '<button onclick="downvote_answer('+answer_id+')">Downvote</button>';
      $('#downvote_'+answer_id).html(html);
    });
}

function upvote_answer(answer_id){
  $.get('forum/upvote_answer/',
    {
      'answer_id': answer_id
    },function(data)
    {
      var html = '<button onclick="remove_upvote('+answer_id+')">Upvoted</button>';
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
      var html = '<button onclick="remove_downvote('+answer_id+')">Downvoted</button>';
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
      var html = '';
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

function display_activity(single,username){
  $.get('forum/fetch_activity/',
    {
      'single': single,
      'username': username
    },function(data)
    {
      var html = '<div id="forum-feed">' ;
      for(i=data.activities.length;i>0;i--)
      {
        html += activities_html(data,i-1);
      }
      html += '</div>'; //forum-feed
      $('#content').html(html);
      $('#content').pickify_users();
      var category_name = "all";
      change_active_label(category_name);
    });
}

function follow_tag(tag_name){
  $.get('forum/follow_tag/',
    {
      'tag_name': tag_name
    },function(data)
    {
      var html =  '<button onclick=\"unfollow_tag(\''+tag_name+'\')\"> Unfollow </button>';
      $('#follow_unfollow_tag_'+escapeStr(tag_name)).html(html);
    });
}

function unfollow_tag(tag_name){
  $.get('forum/unfollow_tag/',
    {
      'tag_name': tag_name
    },function(data)
    {
      var html =  '<button onclick=\"follow_tag(\''+tag_name+'\')\"> Follow </button>';
      $('#follow_unfollow_tag_'+escapeStr(tag_name)).html(html);
    });
}

function search_tag(){
  $.post('forum/search_tag/',
    {
      'tag_key': $('input[name=tag_key]').val()
    },function(data)
    {
      var html = '';
      for(i=data.tags.length;i>0;i--)
      {
        html += '<div id = "tag_'+data.tags[i]+'"><a href="#forum/tag/'+data.tags[i]+'">' + data.tags[i] + '</a></div>';
      }
      $('#content').append(html);
    });
}

function show_comments(answer_id){
  $('#show_hide_comments_'+answer_id).remove();
  $('#answer_comments_'+answer_id).load('forum/answer_comments/'+answer_id);
  var html = '<div id="show_hide_comments_'+answer_id+'" onclick="hide_comments('+answer_id+')"> Hide Comments </div>';  
  $('#comments_'+answer_id).prepend(html);
}

function hide_comments(answer_id){
  $('#answer_comments_'+answer_id).html('');
  var html = 'show comments';
  $('#show_hide_comments_'+answer_id).html(html);
  $('#show_hide_comments_'+answer_id).on("click",function(){show_comments(answer_id);});
}

function change_active_label(category_name){
      $('#all'). removeClass('active-label');
      $('#unanswered').removeClass('active-label');
      $('#mytopic').removeClass('active-label');
      $('#popular').removeClass('active-label');
      $('#'+category_name). addClass('active-label');
}

function display_category(type_question){
  $.get('forum/fetch_questions/',
    {
      'type_question': type_question
    },function(data)
    {
      var html = '<div id="forum-feed">';
      for(var i=data.questions.length;i>0;i--)
      {
        html +=  questions_html(data,i-1,type_question);
      }
      html += '</div>'; //forum-feed
      $('#content').html(html);
      $('#content').pickify_users();
      var category_name = location.hash.substr(1).split('/')[1];
      change_active_label(category_name);
    });
}
/*
function display_question_followers(question_id){
  $.get('forum/fetch_question_followers/',
    {
      'question_id': question_id
    },function(data)
    {
  */    
