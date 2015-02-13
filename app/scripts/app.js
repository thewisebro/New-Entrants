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
    'ui.router',
    'ui.bootstrap',
    'datatables'
  ]);


/**
 * /course : common course page to be viewed
 * /course/:course-id : A particular course page with all details
 */
// Django integration. 
lectutApp.config( ['$interpolateProvider',function($interpolateProvider){
    console.log("daddy starts");
    $interpolateProvider.startSymbol("{[").endSymbol("]}");
    console.log("daddy ends");
  }]);

lectutApp.config(['$stateProvider', '$urlRouterProvider','$locationProvider',
  function($stateProvider, $urlRouterProvider, $locationProvider) {
    
     $urlRouterProvider.otherwise("/");
     
     $stateProvider
        .state('/',{
           url: "/",
           templateUrl: '/views/partials/common-course-home.html',
           controller: 'CourseHomeCtrl'         
        })
        .state('course', {
           url: "course/:courseId",
           templateUrl: '/views/partials/course-detail.html',
           controller: 'CourseDetailCtrl'
         })
        .state('course.feeds', {
           url: "/feeds",
           templateUrl: '/views/partials/course-feeds.html',
           controller: 'CourseFeedsCtrl'
         })
        .state('course.files', {
           url: "/files",
           templateUrl: '/views/partials/course-files.html',
           controller: 'CourseFilesCtrl'
         })
         .state('course.members', {
           url: "/members",
           templateUrl: '/views/partials/course-members.html',
           controller: 'CourseMembersCtrl'
         });
    /*
    $routeProvider.
      when('/', {
        templateUrl: '/views/partials/common-course-home.html',
        controller: 'CourseHomeCtrl'
      }).
      when('/course/:courseId/', {
        templateUrl: '/views/partials/course-detail.html',
        controller: 'CourseDetailCtrl'
      }).
      when('/course/:courseId/feeds', {
        templateUrl: '/views/partials/course-detail.html',
        controller: 'CourseDetailCtrl'
      }).
      when('/course/:courseId/files', {
        templateUrl: '/views/partials/course-detail.html',
        controller: 'CourseDetailCtrl'
      }).
      when('/course/:courseId/members', {
        templateUrl: '/views/partials/course-detail.html',
        controller: 'CourseDetailCtrl'
      }).
      otherwise({
        redirectTo: '/'
      });*/
    $locationProvider.html5Mode(true);
  }]);

