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
    'ngRoute'
  ]);


/**
 * /course : common course page to be viewed
 * /course/:course-id : A particular course page with all details
 */

lectutApp.config(['$routeProvider', '$locationProvider',
  function($routeProvider, $locationProvider) {
    $routeProvider.
      when('/', {
        templateUrl: '/views/partials/common-course-home.html',
        controller: 'CourseHomeCtrl'
      }).
      when('/course/:courseId', {
        templateUrl: '/views/partials/course-detail.html',
        controller: 'CourseDetailCtrl'
      }).
      otherwise({
        redirectTo: '/'
      });
    
    $locationProvider.html5Mode(true);
  }]);
