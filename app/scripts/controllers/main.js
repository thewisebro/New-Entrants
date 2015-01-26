'use strict';

/**
 * @ngdoc function
 * @name lectutApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the lectutApp
 */
lectutApp
  .controller('MainCtrl', function ($scope) {

    //current user details
    $scope.userdetails = {
     username:"Himanshu Jariyal",
     enrollmentNo:"12114030",
     branch:"CSE"  
    };
   
    //course name of current user
    $scope.courses = [
    {
      name:"Electronics and Communication",
      id:"EC-101",
      notifications:5
    },
    {
      name:"Physics",
      id:"CC-301",
      notifications:3
    }, 
    {
      name:"Business Managemnet",
      id:"ME-401",
      notifications:2
    }, 
    {
      name:"Fine arts and music",
      id:"REC-101",
      notifications:1
    },
    {
      name:"Hardware Lab",
      id:"WE-161",
      notifications:5
    }
    ];
  });

lectutApp.controller('CourseHomeCtrl', ['$routeParams', function($routeParams) {
  this.params = $routeParams;
}]);

lectutApp.controller('CourseDetailCtrl', ['$routeParams','$scope', function($routeParams,$scope) {
  this.params = $routeParams;
  $scope.coursename = this.params.courseId;
}]);

