jQuery(function($) {
  var tour = new Tour({
    useLocalStorage:true,
  });
  tour.addStep({
    element: "#feeds-content-tab",
    placement: "top",
    title: "Welcome to Bootstrap Tour!",
    content: "Introduce new users to your product by walking them "
             + "through it step by step. Built on the awesome "
  });
  tour.start();
});
