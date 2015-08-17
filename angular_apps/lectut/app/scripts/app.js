'use strict';

/**
 * @ngdoc overview
 * @name lectutApp
 * @description
 * # lectutApp
 *
 * Main module of the application.
 */
var lectutApp = angular.module('lectutApp', [
    'ngAnimate',
    'ngRoute',
    //'ui.router',
    'ui.bootstrap',
    'datatables',
    'ngCookies',
    'angularFileUpload',
    'angularMoment',
    'angular-loading-bar',
    'infinite-scroll',
    'oitozero.ngSweetAlert',
    'ngNotify'
  ]);


/**
 * /course : common course page to be viewed
 * /course/:course-id : A particular course page with all details
 */
// Django integration. 
lectutApp.config( ['$interpolateProvider', '$httpProvider',function($interpolateProvider, $httpProvider){
    //console.log("daddy starts");
    $interpolateProvider.startSymbol("{[").endSymbol("]}");
    //console.log("daddy ends");
    $httpProvider.defaults.withCredentials = true;
  }]);

lectutApp.config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
       cfpLoadingBarProvider.includeSpinner = false;
}]);



lectutApp.config(['$locationProvider','$routeProvider',
  function( $locationProvider, $routeProvider) {
   
    
   $routeProvider.
      when('/', {
        templateUrl: 'views/partials/common-course-home.html',
        controller: 'CourseHomeCtrl'
      }).
      /*when('/course/:courseId/', {
        templateUrl: 'views/partials/course-detail.html',
        controller: 'CourseDetailCtrl'
      }).*/
      when('/course/:courseId/feeds', {
        templateUrl: 'views/partials/course-feeds.html',
        controller: 'CourseDetailCtrl'
      }).
      when('/course/:courseId/files', {
        templateUrl: 'views/partials/course-files.html',
        controller: 'CourseFilesCtrl'
      }).
      when('/course/:courseId/members', {
        templateUrl: 'views/partials/course-members.html',
        controller: 'CourseMembersCtrl'
      }).
      when('/course/:courseId/feeds/:postId', {
        templateUrl: 'views/partials/one-post.html',
        controller: 'CourseOnePostCtrl'
      }).
      when('/course/:courseId/files/:fileId', {
        templateUrl: 'views/partials/one-file.html',
        controller: 'CourseOneFileCtrl'
      }).
      when('/faculty/:facultyId', {
        templateUrl: 'views/partials/faculty.html',
        controller: 'FacultyCtrl'
      }).
      otherwise({
        redirectTo: '/'
      });
    //$locationProvider.html5Mode(true);
  }]);

