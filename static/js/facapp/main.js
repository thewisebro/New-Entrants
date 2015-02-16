$(document).ready(function(){

	$("#tabs ul").on('click', 'li', function() {
		if($(this).hasClass("active")){
		}
		else{

			$(this).addClass("active");
			$(this).siblings().removeClass("active");

			text = $.trim($(this).text()).split(' ').join('_').toLowerCase();
			id = "#" + text;
			// console.log(id);
			$(id).removeClass("hidden");
			$(id).siblings().addClass("hidden");
	    }
	});
	
	$( "#sortable" ).sortable({
		revert      : 'invalid',
		placeholder : 'placeholder',
		update      : function (event, ui) {
			var priority="";
			$("#sortable li").each(function(i) {
				if (priority=='')
					priority = $(this).text();
				else
					priority += "," + $(this).text();
			});
      inputs = {
        'priority' : priority,
      }
      $.ajax({
        data: inputs,
        dataType: 'html',
        type: 'POST',
        url: '/facapp/setPriority/',
        success: function(data){
        },
        error: function(){
          console.log('error occurred');
        }
      });
			console.log(priority);
		},
	});
	$( "#sortable" ).disableSelection();

});




function updateSection(elem){
    var classy = $(elem).attr("ht");
    var inputs = {
        "title" : classy,
        "content" : $("[id='" + classy + "']").html(),
    };
          $.ajax({
            data: inputs,
            dataType: 'html',
            type: "POST",
            url: "",
            success: function(data){
            $("#" + classy).html(data);
            }
          });
          return false;
}


function show_titles(){
  $("#titles_list").css("display","block");
}


function get_fields(elem){
  console.log("sent");
  title = $(elem).html();
  console.log(title);
  var inputs = {
    "title" : title,
  };
  $.ajax({
    data: inputs,
    datatype: 'html',
    type: "POST",
    url: "/facapp/fields/" + title + "/",
    success: function(data){
      title_id = title.split(' ').join('_').toLowerCase();
      $("#new_sections").append('<div id="' + title_id + '" ></div>');
      console.log(title_id);
      $("#" + title_id).attr({
        contentEditable:"true",
      });
      $("#" + title_id ).append(title + "<br /><br />");
      res = data.split(',');
      len = res.length-1;
      for(var i = 0; i < len ; i++)
      {
        field = res[i].split(':');
        $("#" + title_id ).append(field[0] + " dummy content <br />");
      }
      CKEDITOR.inline(title_id);

      $("#new_sections").append('<input> <button ht="' + title + '" type="submit" name="submit" onclick="return createSection(this)" >save</button> <br /><br />');
    } 
  });
}


function createSection(elem){
  var title = $(elem).attr("ht");
  var title_id = title.split(' ').join('_').toLowerCase();
  var content = $("#" + title_id).html();
  var priority = $("#new_sections").find("input").html();
  console.log(priority);
  var inputs ={
    "title" : title,
    "content" : content,
    "priority" : priority,
  };
  $.ajax({
    data: inputs,
    dataType: 'html',
    type: "POST",
    url: "/facapp/createSection/",
    success: function(data){
      console.log("done");
    }
  });
}

