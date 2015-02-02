'use strict';
var thing;
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
     username:'Himanshu Jariyal',
     enrollmentNo:"12114030",
     branch:"B.Tech CSE 3rd Year"  
    };
   
    $scope.users =[
    {
      url:"https://avatars2.githubusercontent.com/u/552817?v=3&s=80"
    },
    {
      url:"https://avatars0.githubusercontent.com/u/2171796?v=3&s=80"
    },
    {
      url:"https://avatars3.githubusercontent.com/u/810438?v=3&s=80"
    }
    ];
    //course name of current user
    $scope.courses = [
    {
      name:"Electronics and Communication",
      id:"EC-131",
      notifications:5
    },
    {
      name:"Physics",
      id:"PH-101",
      notifications:3
    }, 
    {
      name:"Business Managemnet",
      id:"BM-002",
      notifications:2
    }, 
    {
      name:"Fine arts and music",
      id:"FA-102",
      notifications:1
    },
    {
      name:"Hardware Lab",
      id:"EC-332",
      notifications:5
    }
    ];
  });

lectutApp.controller('CourseHomeCtrl', ['$routeParams', function($routeParams) {
  this.params = $routeParams;
}]);

lectutApp.controller('CourseDetailCtrl', ['$stateParams','$route','$scope','CourseDetails',function($stateParams,$route,$scope,CourseDetails) {
  this.params = $stateParams;
  $scope.courseId = this.params.courseId;
  $scope.courseName = "Physics and Chemistry";
  
  var promiseCourseData = CourseDetails.getCourseDetailsData();
  promiseCourseData.then(function (d) {
     $scope.posts = d.data[0].posts;
     console.log($scope.posts);  
  });
}]);

lectutApp.controller('CourseFeedsCtrl', ['$stateParams','$scope', function($stateParams,$scope) {

}]);

lectutApp.controller('CourseFilesCtrl', ['$stateParams', function($stateParams) {
  this.params = $stateParams;
}]);
lectutApp.controller('CourseMembersCtrl', ['$stateParams', function($stateParams) {
  this.params = $stateParams;
}]);
