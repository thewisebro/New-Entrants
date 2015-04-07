'use strict';

var app = angular.module('yaadeinApp');
var baseURL = base_domain + '/yaadein_api';

app.service('TickerService', ['$http', '$q', function ($http, $q) {
    this.getTrending = function () {
        var deferred = $q.defer();
        var url = baseURL + '/trending/';
        $http.get(url)
          .success(function (x) {
            deferred.resolve(x);
          });
        return deferred.promise;
    };

    this.inviteUsers = function (x) {
      var q = $q.defer();
      var URL = baseURL + '/invite/';
      $http({
        method: 'POST',
        url: URL,
        headers: {'Content-Type':'multipart/form-data'},
        data: {
          user_tags: x
        },
        file: []
      }).success(function (d) {
          q.resolve(d);
        });
      return q.promise;
    };
}]);

app.service('HomeService', ['$http', '$q', function ($http, $q) {
	var deferred = $q.defer();
  var url = baseURL + '/home/';
	$http.get(url)
		.success(function (d) {
			deferred.resolve(d);

      //Add baseURL to image URLs
      d.profilePic = baseURL + d.profilePic;
      d.coverPic = originURL + d.coverPic;
      var posts = d.posts_data;
      for (var i = 0; i < posts.length; i += 1) {
        posts[i].post_owner_pic = originURL + posts[i].post_owner_pic;
        for (var j = 0; j < posts[i].image_url.length; j += 1) {
          posts[i].image_url[j] = originURL + posts[i].image_url[j];
        }
      }
		});

	this.getLoggedUser = function () {
		return deferred.promise;
	};

}]);

app.service('UserService', ['$http', '$q', function ($http, $q) {

	this.getUser = function (enrolmentNo) {
		var def = $q.defer(), url;
    if (!isNaN(enrolmentNo)) {
		  url = baseURL + '/user/' + enrolmentNo.toString() + '/';
    } else {
      url = baseURL + '/spot/' + enrolmentNo.toString() + '/';
    }
    $http.get(url)
      .success(function (x) {
        def.resolve(x);
    });
		return def.promise;
	};

}]);

app.service('HashtagService', ['$http', '$q', function ($http, $q) {

    this.getHashtaggedPosts = function (tag) {
        var deferred = $q.defer();
        var url = baseURL + '/tag/' + tag + '/';
        $http.get(url)
          .success(function (x) {
            deferred.resolve(x);
          });
        return deferred.promise;
    };

}]);

app.service('PostService', ['$http', '$q', function ($http, $q) {

    this.getPost = function(id) {
      var def = $q.defer();
      var url = baseURL + '/post_disp/' + id + '/';
      $http.get(url)
        .success(function (x) {
          def.resolve(x);
      });
      return def.promise;
    };

    this.deletePost = function(id) {
      var def = $q.defer();
      var url = baseURL + '/delete/' + id + '/';
      $http.get(url)
        .success(function (x) {
          def.resolve(x);
      });
      return def.promise;
    };
}]);
