/*!function ($) {

  "use strict"; // jshint ;_;
 
 TAB DATA-API
  * ============ 

  $(function () {
    $('body').on('click.tab.data-api', '[data-toggle="tab"], [data-toggle="pill"]', function (e) {
      e.preventDefault()
      $(this).tab('show')
    })
  })
}(window.jQuery);
*/
$(document).ready(function(){
     $('.dropdownArrow').click(function(){
        $(this).parent().next().next().toggle(300);
        //alert("df");

       });
     
    });
