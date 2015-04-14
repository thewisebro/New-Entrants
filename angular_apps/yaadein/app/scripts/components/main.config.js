'use strict';

var app = angular.module('yaadeinApp');

var resolve = {
  delay: function ($q, $timeout) {
    var delay = $q.defer();
    $timeout(delay.resolve, 50, false);
    return delay.promise;
  }
};

app.config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
    cfpLoadingBarProvider.latencyThreshold = 0;
    cfpLoadingBarProvider.includeBar = false;
    cfpLoadingBarProvider.parentSelector = '#yaadein-title';
}]);

app.config(['LightboxProvider', function (LightboxProvider) {
    LightboxProvider.templateUrl = 'views/lightbox.html';
    LightboxProvider.getImageUrl = function (imageUrl) {
    return imageUrl;
  };
}]);

app.config(['$locationProvider', '$routeProvider', function ($locationProvider, $routeProvider) {
	$routeProvider
	.when('/', {
		templateUrl: '/yaadein/views/home.html',
		controller: 'HomeController',
		resolve: resolve
	})
	.when('/profile/:enrolmentNo', {
		templateUrl: '/yaadein/views/profile.html',
		controller: 'ProfileController',
		resolve: resolve
	})
	.when('/spots/', {
		templateUrl: '/yaadein/views/spots.html',
		controller: 'SpotsController',
		resolve: resolve
	})
	.when('/hashtag/:hashtag', {
		templateUrl: '/yaadein/views/hashtag.html',
		controller: 'HashtagController',
		resolve: resolve
	})
	.when('/post/:postId', {
		templateUrl: '/yaadein/views/post.html',
		controller: 'PostController',
		resolve: resolve
	})
	.otherwise({
		redirectTo: '/'
	});

  //$locationProvider.html5Mode(true).hashPrefix('!');
	
}]);

app.config(['$interpolateProvider', '$httpProvider', function ($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('{~{').endSymbol('}~}');
    $httpProvider.defaults.withCredentials = true;
}]);

//app.run(['$http', '$cookies', function ($http, $cookies) {
//    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
//}]);
