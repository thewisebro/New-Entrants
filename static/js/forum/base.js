$(document).on("load_app_forum",function(e,hash1,hash2,hash3,hash4){
    if(!hash1) $('#content').html('forum under construction!');
    if(hash1 == 'question') display_question(hash2);
});

function display_question(id){
}
