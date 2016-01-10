
  function loadingComplete()
  {
   /* if ($(".input-button").length)
    {
      parent.$(".ui-dialog-titlebar-close").css("display","none");
    }
   */


    //this function removes the bug in which item options of my-account page behaved improperly and their visibility toggled irrationally

    var hideOverlay=function()
    {
      $(".full-page-transparent-overlay").css("display","none");
    };
    setTimeout(hideOverlay, 50);

    //visibility bugfix ends

    $(".alert-error").centerHorizontally();

    var hideAlert=function()
    {
      $(".alert").fadeOut();
    };

    setTimeout(hideAlert, 5000);

    var widthOfWindow= $(window).width();
    $(".headerBackground").css("width",widthOfWindow+"px");

    var attr = $(this).attr('name');
    if (typeof attr !== typeof undefined && attr !== false)
    {

    }

    var subHeaderWidth= $(".sub-header").width();
    $(".page-content").css("width",subHeaderWidth-275+"px");
    if(subHeaderWidth >= 1100)
    {
      $(".item-for-sale-image").css("height",160+"px");
      $(".search-area").css("margin-left",30+"px");
      $(".search-area").css("width",41.5+"%");
    }

    else if(subHeaderWidth >= 900)
    {
      $(".item-for-sale-image").css("height",120+"px");
      $(".search-area").css("margin-left",30+"px");
      $(".search-area").css("width",41.5+"%");
      $(".itemName").css("width",80+"px");
    }

    else if(subHeaderWidth >= 750)
    {
      $(".item-for-sale-image").css("height",181+"px");
      $(".search-area").css("margin-left",-120+"px");
      $(".search-area").css("width",55+"%");
      $(".itemName").css("width",80+"px");
    }

    $(window).resize
    (
      function()
      {
        var newWidthOfWindow= $(window).width();
        $(".headerBackground").css("width",newWidthOfWindow+"px");
        var subHeaderWidth= $(".sub-header").width();
        $(".page-content").css("width",subHeaderWidth-275+"px");
        //console.log(subHeaderWidth);
        if(subHeaderWidth >= 1100)
        {
          $(".item-for-sale-image").css("height",160+"px");
          $(".search-area").css("margin-left",30+"px");
          $(".search-area").css("width",41.5+"%");
        }
        else if(subHeaderWidth >= 900)
        {
          $(".item-for-sale-image").css("height",120+"px");
          $(".search-area").css("margin-left",30+"px");
          $(".search-area").css("width",41.5+"%");
          $(".itemName").css("width",80+"px");
        }
        else if(subHeaderWidth >= 750)
        {
          $(".item-for-sale-image").css("height",181+"px");
          $(".search-area").css("margin-left",-120+"px");
          $(".search-area").css("width",55+"%");
          $(".itemName").css("width",80+"px");
        }

        if ($(".page-content").height() < $(window).height() - 181 )
        {
          $(".pagination").addClass("pagination-bottom-aligned");
        }
   /*     else
        {
          $(".pagination-customized").css("margin-left","40%");
        }
  */
        }
    );

    //Give bottom shadow to header-background on scrolldown
    $(window).scroll
    (
      function()
      {
        var scroll = $(window).scrollTop();
        if (scroll > 0)
        {
          $("#header").addClass("active");
        }
        else
        {
          $("#header").removeClass("active");
        }
      }
    );



    $(document).click
    (
      function ()
      {
        if($("#filter-by-category").hasClass("open"))
        {
          $(".dropdown-arrow",$(this)).addClass("dropdown-arrow-pointing-down");
          $(".active-category",$(this)).addClass("active-category-dropdown-active");
        }
        else
        {
          $(".dropdown-arrow",$(this)).removeClass("dropdown-arrow-pointing-down")
          $(".active-category",$(this)).removeClass("active-category-dropdown-active");
        }
      }
    );

  /*  $(".item").click
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
*/
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

    $(".get-shareable-url-button").click
    (
      function()
      {
        $(this).css("display","none")
        $(".shareable-url-text-box").css("display", "inline");
        $(".shareable-url-text-box").select();
      }
    );
    $(".shareable-url-text-box").click
    (
      function()
      {
        $(this).select();
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
          ,0);
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

    $("#slider-range a:first-child").css("z-index","2");


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

    /*
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
    */


    $(".phone-no-visibility-toggle , .phone-no-visibility-toggle-button").toggle
    (
      function()
      {
        $(".phone-no-visibility-toggle-button").addClass("phone-no-visibility-toggle-button-hidden",400);
        $(".phone-no-visibility-toggle-slider").addClass("phone-no-visibility-toggle-slider-hidden",400);
      },

      function()
      {
        $(".phone-no-visibility-toggle-button").removeClass("phone-no-visibility-toggle-button-hidden",400);
        $(".phone-no-visibility-toggle-slider").removeClass("phone-no-visibility-toggle-slider-hidden",400);
      }
    );



 /*   $(".thumbnailBG-my-account").click
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
*/
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
          ,0);
      }
    );

    $("#buyer").change
    (
      function() {
        if ($('#buyer').val() == "Other") {
          $('#other-person-option-clicked').show();
        }
        else {
          $('#other-person-option-clicked').hide();
        }
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

