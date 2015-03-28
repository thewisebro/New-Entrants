'use strict';
var app = angular.module('lectutApp');
app.service('CourseDetails', ['$http', '$q','$cookies',
      function ($http, $q, $cookies) {
       var deferred;
       var csrf = $cookies.csrftoken;
        var channeli_sessid = $cookies.CHANNELI_SESSID;
       this.getCourseDetailsData = function (id) {
         deferred = $q.defer();
         /*$http.post({
            url: myUrl,
            crossDomain: true,
            method: "POST",
            headers: {
              'Authorization': 'Basic dGVzdDp0ZXN0',
              "user": "harshithere"
            }
           }).success(function (d) {*/
         /*var req = {
            method: 'POST',
            url: 'http://172.25.55.156:60001/lectut_api/ajax/3/',
            headers: {
              'Content-Type': undefined
            },
            data: { "CHANNELI_SESSID": channeli_sessid }
         }
         $http(req).success(function(d){  */

         //$http.get(myUrl).success(function (d){
         $http.post(base_domain+'/lectut_api/feeds/'+id+'/').success(function (d) {
             console.log("this is full content.");
             console.log(d);
          deferred.resolve(d);
         }).error(function(d){
            console.log("error");
         });
        return deferred.promise;
      };
}]);

app.service('FeedFileDownload', ['$http', '$q','$cookies',
      function($http,$q,$cookies){
       var deferred;
       var csrf = $cookies.csrftoken;

       this.getFeedFile = function (id) {
          deferred = $q.defer();
          // Append / after the request because Shubham Sir has written this on django docs for security reasons.
          var urlSend = base_domain+'/lectut_api/download/'+id+'/';
          console.log(urlSend);
          $http.post(urlSend).success(function(d){
          //console.log(d);
          deferred.resolve(d);
         }).error(function(d){
            console.log("error");
         });
        return deferred.promise;
      };
}]);


app.service('RemoveFeedPost', ['$http', '$q','$cookies',
      function($http,$q,$cookies){
       var deferred;
       var csrf = $cookies.csrftoken;

       this.deleteFeedPost = function (id) {
          deferred = $q.defer();
          // Append / after the request because Shubham Sir has written this on django docs for security reasons.
          var urlSend = base_domain+'/lectut_api/deletePost/'+id+'/';
          console.log(urlSend);
          $http.post(urlSend).success(function(d){
          //console.log(d);
          deferred.resolve(d);
         }).error(function(d){
            console.log("error");
         });
        return deferred.promise;
      };
}]);

app.service('RemoveFeedFile', ['$http', '$q','$cookies',
      function($http,$q,$cookies){
       var deferred;
       var csrf = $cookies.csrftoken;
      
       this.deleteFeedFile = function (id) {
          deferred = $q.defer();
          // Append / after the request because Shubham Sir has written this on django docs for security reasons.
          var urlSend = base_domain+'/lectut_api/deleteFile/'+id+'/';
          console.log(urlSend);
          $http.post(urlSend).success(function(d){
          //console.log(d);
          deferred.resolve(d);
         }).error(function(d){
            console.log("error");
         });
        return deferred.promise;
      };
}]);
app.service('DataTables', ['$http','$q',
      function($http, $q){
        var deferred;
          this.getTable = function(id){
          var urlSend = base_domain+'/lectut_api/files/'+id+'/'; 
          deferred = $q.defer();
           $http.post(urlSend).success(function(d){
          //$http.get('http://beta.json-generator.com/api/json/get/FQlO35E').success(function (d) {
         // console.log(d);
          deferred.resolve(d);
          }).error(function(d){
            console.log("error");
          });
          return deferred.promise;
        };
}]);

app.service('Members', ['$http','$q',
      function($http, $q){
        var deferred;
          this.getMembers = function(id){
          var urlSend = base_domain+'/lectut_api/members/'+3+'/'; 
          deferred = $q.defer();
           $http.post(urlSend).success(function(d){
          deferred.resolve(d);
          }).error(function(d){
            console.log("error");
          });
          return deferred.promise;
        };
}]);

app.service('LoadFeed', ['$http','$q',
      function($http, $q){
        var deferred;
          this.loadFeed = function(id){
          var urlSend = base_domain+'/lectut_api/feeds/'+id+'/'; 
          deferred = $q.defer();
          $http.post(urlSend, {dataId: id}).success(function(d){
              deferred.resolve(d);
          }).error(function(d){
            console.log("error");
          });
          return deferred.promise;
        };
}]);

app.service('LoadOnePost', ['$http','$q',
      function($http, $q){
        var deferred;
          this.getOnePost = function(postId){
          var urlSend = base_domain+'/lectut_api/feeds/'+3+'/'+ postId+'/';
          deferred = $q.defer();
          $http.post(urlSend).success(function(d){
              deferred.resolve(d);
          }).error(function(d){
            console.log("error");
          });
          return deferred.promise;
        };
}]);


app.service('SearchService', ['$http','$q',
      function($http, $q){
        var deferred;
          console.log("s");
          this.getSearchData = function(qs){
          var urlSend = base_domain+'/lectut_api/search/?q='+qs;
          deferred = $q.defer();
          $http.post(urlSend).success(function(d){
              deferred.resolve(d);
          }).error(function(d){
            console.log("error");
          });
          return deferred.promise;
        };
}]);

app.service('InitialSetup', ['$http','$q',
      function($http, $q){
        var deferred;
          //console.log("s");
          this.getInitialData = function(){
          var urlSend = base_domain+'/lectut_api/';
          deferred = $q.defer();
          $http.post(urlSend).success(function(d){
              deferred.resolve(d);
          }).error(function(d){
            console.log("error");
          });
          return deferred.promise;
        };
}]);

app.service('Comments', ['$http','$q',
      function($http, $q){
        var deferred;
          //console.log("s");
          this.getComments = function(postId){
          var urlSend = base_domain+'/lectut_api/comments/'+postId+'/';
          deferred = $q.defer();
          $http.post(urlSend).success(function(d){
              deferred.resolve(d);
          }).error(function(d){
            console.log("error");
          });
          return deferred.promise;
        };
}]);
