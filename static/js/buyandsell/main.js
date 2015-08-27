jQuery.fn.center = function () {
  this.css("position","absolute");
  this.css("top", Math.max(0, (($(window).height() - $(this).outerHeight()) / 2) + $(window).scrollTop()) + "px");
  this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) +  $(window).scrollLeft()) + "px");
  return this;
}


$(document).ready
(
  function()
  {
    var widthOfWindow= $(window).width()
    $(".headerBackground").css("width",widthOfWindow+"px");

    var attr = $(this).attr('name');
    if (typeof attr !== typeof undefined && attr !== false)
    {

    }

    $(window).resize
    (
      function()
      {
        var newWidthOfWindow= $(window).width();
        $(".headerBackground").css("width",newWidthOfWindow+"px");
      }
    );

    //Give bottom shadow to header-background on scrolldown
    $(window).scroll(function() {
      var scroll = $(window).scrollTop();
      if (scroll > 0) {
        $("#header").addClass("active");
      }
      else {
        $("#header").removeClass("active");
      }
    });

    $(".item").click
    (
      function() //opens light box with details for the clicked item-for-sale
      {
        var modalHead = $(".itemName", $(this)).html();
        //console.log(modalHead);
        $(".modal-title").html(modalHead);
        var modalImage = $((".thumbnail img"), $(this)).attr("src");
        //console.log(modalImage);
        $(".modal-image").attr("src",modalImage);
        var modalPrice = $("div .price", $(this)).html();
        //console.log(modalPrice);
        $(".modal-price").html(modalPrice);
      }
    );

    $(".request").click
    (
      function() //opens light box with details for the clicked request
      {
        var modalHead = $(".requested-item-name", $(this)).html();
        //console.log(modalHead);
        $(".modal-title").html(modalHead);
        var modalPrice = $(".requested-item-price", $(this)).html();
        //console.log(modalPrice);
        $(".modal-max-price").html(modalPrice);
      }
    );

    $(".instant-searched-item-for-sale").click
    (
      function() //opens light box with details for the clicked item-for-sale
      {
        var modalHead = $(".searched-item-name", $(this)).html();
        //console.log(modalHead);
        $(".modal-title").html(modalHead);
        var modalPrice = $(".searched-item-price", $(this)).html();
        //console.log(modalPrice);
        $(".modal-price").html(modalPrice);
      }
    );

    $(".instant-searched-request").click
    (
      function() //opens light box with details for the clicked item-for-sale
      {
        var modalHead = $(".searched-item-name", $(this)).html();
        //console.log(modalHead);
        $(".modal-title").html(modalHead);
        var modalPrice = $("div .searched-item-price", $(this)).html();
        //console.log(modalPrice);
        $(".modal-max-price").html(modalPrice);
      }
    );

    $(".enquire").click
    (
      function()
      {
        $(".enquire-clicked")
          .css('opacity', 0)
          .slideDown(400)
          .animate
        (
          { opacity: 1 },
          { queue: false, duration: 400 }
        );
        setTimeout
        (
          function()
          {
            $(".enquire").css("display","none");
            $(".send").css("display","inline");
          }
          ,400);
      }
    );
    $("#item-for-sale-modal").on
    ('hidden.bs.modal',
      function ()
      {
        $(".enquire-clicked").fadeOut();
        $(".enquire").css("display","inline");
        $(".send").css("display","none");
      }
    );
    $("#request-modal").on
    ('hidden.bs.modal',
      function ()
      {
        $(".enquire-clicked").fadeOut();
        $(".enquire").css("display","inline");
        $(".send").css("display","none");
      }
    );


    $(document).mouseup
    (
      function(x)
      {
        var box = $(".search-area");
        if(!box.is(x.target)// if the target of the click isn't the box...
          && box.has(x.target).length===0) //... nor a descendant of the box
        {
          $(".search-result-box").hide();
        }
      }
    );

    $(".search-form").keyup
    (
      function()
      {
        var searchedQuery=$(".search-form").val();
        if ( searchedQuery.length > 0 && searchedQuery != "What are you looking for..." )
        {
          $(".search-result-box").css("display", "block");
          $(".searched-query").html(searchedQuery);
        }
        else
        {
          $(".search-result-box").css("display", "none");
        }
      }

    );

    $(".search-form").click
    (
      function()
      {
        var searchedQuery=$(".search-form").val();
        if ( searchedQuery.length > 0 && searchedQuery != "What are you looking for..." )
        {
          $(".search-result-box").css("display", "block");
          $(".searched-query").html(searchedQuery);
        }
        else
        {
          $(".search-result-box").css("display", "none");
        }
      }

    );

    $(".sell-form-item-name").keyup
    (
      function()
      {
        $(".sell-form-search-result-box").css("display","block");
        var searchedQuery=$(".search-form").val();
        $(".searched-query").html(searchedQuery);
      }
    );

    $(document).mouseup
    (
      function(x)
      {
        var box = $(".sell-form-item-name-area");
        if(!box.is(x.target)// if the target of the click isn't the box...
          && box.has(x.target).length===0) //... nor a descendant of the box
        {
          $(".sell-form-search-result-box").hide();
        }
      }
    );

    $(".search-form").keyup
    (
      function()
      {
        $(".sell-form-search-result-box").css("display","block");
        //var searchedQuery=$(".search-form").val();
        //$(".searched-query").html(searchedQuery);
      }

    );
    // Code for the price range selector (starts)

    /*	$( "#low" ).val
     (
     $( "#slider-range" ).slider( "values", 0 )
     );

     $( "#high" ).val
     (
     $( "#slider-range" ).slider( "values", 1 )
     );
     // Code for the price range selector (ends)*/


    //Code to show the edit button when the item is hovered in my account page
    $(".thumbnailBG").mouseover
    (
      function()
      {
        $(".edit-button", $(this)).css('opacity', 1);
        $(".item-remove-button", $(this)).css('opacity', 1);
      }
    );
    $(".thumbnailBG").mouseout
    (
      function()
      {
        $(".edit-button", $(this)).css('opacity', 0);
        $(".item-remove-button", $(this)).css('opacity', 0);
      }
    );

    $(".request").mouseover
    (
      function()
      {
        $(".edit-button", $(this)).css('opacity', 1);
        $(".request-remove-button", $(this)).css('opacity', 1);
      }
    );
    $(".request").mouseout
    (
      function()
      {
        $(".edit-button", $(this)).css('opacity', 0);
        $(".request-remove-button", $(this)).css('opacity', 0);
      }
    );

    $(".thumbnailBG-my-account").click
    (
      function() //opens light box with details for the clicked item-for-sale
      {
        //var modalHead = $(".caption .itemName", $(this)).html();
        //console.log(modalHead);
        $(".modal-title").html(modalHead);
        var modalImage = $((".thumbnail img"), $(this)).attr("src");
        //console.log(modalImage);
        $(".modal-image").attr("src",modalImage);
        var modalPrice = $("div .price", $(this)).html();
        //console.log(modalPrice);
        $(".modal-price").html(modalPrice);
      }
    );

    $(".yes").click
    (
      function()
      {
        $(".remove-item-modal-text").css("display","none");
        $(".yes-clicked")
          .css('opacity', 0)
          .slideDown(400)
          .animate
        (
          { opacity: 1 },
          { queue: false, duration: 400 }
        );
        setTimeout
        (
          function()
          {
            $(".yes").css("display","none");
            $(".no").css("display","none");
            $(".done").css("display","inline");
          }
          ,400);
      }
    );

    $(".enquire").click
    (
      function()
      {
        $(".enquire-clicked")
          .css('opacity', 0)
          .slideDown(400)
          .animate
        (
          { opacity: 1 },
          { queue: false, duration: 400 }
        );
        setTimeout
        (
          function()
          {
            $(".enquire").css("display","none");
            $(".send").css("display","inline");
          }
          ,400);
      }
    );

    $('#mailedPeople').change
    (
      function()
      {
        if ($('#YourSelectList').val() == 241) {
          $('#OtherDiv').show();
        }
        else {
          $('#OtherDiv').hide();
        }
      }
    );

    //trying to adjust jquery-dialog height as per form height
  /*  var formHeight = $(".manage-watched-box-form").css("height");
    console.log(formHeight);
    $(".manage-watched-box-body").css("height",formHeight+50+"px");
    var bodyHeight = $(".manage-watched-box-body").css("height");
    console.log(bodyHeight);
  */

  }

);

window.jQuery
(
  function()
  {
    // detect browser scroll bar width
    var scrollDiv = $('<div class="scrollbar-measure"></div>').appendTo(document.body)[0],scrollBarWidth = scrollDiv.offsetWidth - scrollDiv.clientWidth;

    $(document).on
    (
      'hidden.bs.modal', '.modal', function(evt)
      {
        // use margin-right 0 for IE8
        $(document.body).css('margin-right', '');
      }
    )
      .on('show.bs.modal', '.modal', function() {
        // When modal is shown, scrollbar on body disappears.  In order not
        // to experience a "shifting" effect, replace the scrollbar width
        // with a right-margin on the body.
        if ($(window).height() < $(document).height()) {
          $(document.body).css('margin-right', scrollBarWidth + 'px');
        }
      });
  });

