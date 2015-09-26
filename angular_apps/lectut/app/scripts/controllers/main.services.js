'use strict';
var app = angular.module('lectutApp');
app.service('CourseDetails', ['$http', '$q','$cookies','ngNotify',
      function ($http, $q, $cookies, ngNotify) {
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
             //console.log("this is full content.");
             //console.log(d);
          deferred.resolve(d);
         }).error(function(d){
            //console.log("error");
             ngNotify.set('Error fetching course details.', {
              position:'top',
              type:'error',
              duration: 3000
             });

         });
        return deferred.promise;
      };
}]);

app.service('FeedFileDownload', ['$http', '$q','$cookies','ngNotify',

      function($http,$q,$cookies,ngNotify){
       var deferred;
       var csrf = $cookies.csrftoken;

       this.getFeedFile = function (id) {
          deferred = $q.defer();
          // Append / after the request because Shubham Sir has written this on django docs for security reasons.
          var urlSend = base_domain+'/lectut_api/download/'+id+'/';
          //console.log(urlSend);
          $http.post(urlSend).success(function(d){
          //console.log(d);
          deferred.resolve(d);
         }).error(function(d){
            //console.log("error");
             ngNotify.set('Error downloading file.', {
              position:'top',
              type:'error',
              duration: 3000
             });

         });
        return deferred.promise;
      };
}]);


app.service('RemoveFeedPost', ['$http', '$q','$cookies','ngNotify',

      function($http,$q,$cookies,ngNotify){
       var deferred;
       var csrf = $cookies.csrftoken;

       this.deleteFeedPost = function (id) {
          deferred = $q.defer();
          // Append / after the request because Shubham Sir has written this on django docs for security reasons.
          var urlSend = base_domain+'/lectut_api/deletePost/'+id+'/';
          //console.log(urlSend);
          $http.post(urlSend).success(function(d){
          //console.log(d);
          deferred.resolve(d);
         }).error(function(d){
           // console.log("error");
             ngNotify.set('Error removing post.', {
              position:'top',
              type:'error',
              duration: 3000
             });

         });
        return deferred.promise;
      };
}]);

app.service('RemoveFeedFile', ['$http', '$q','$cookies','ngNotify',
      function($http,$q,$cookies,ngNotify){
       var deferred;
       var csrf = $cookies.csrftoken;
      
       this.deleteFeedFile = function (id) {
          deferred = $q.defer();
          // Append / after the request because Shubham Sir has written this on django docs for security reasons.
          var urlSend = base_domain+'/lectut_api/deleteFile/'+id+'/';
          //console.log(urlSend);
          $http.post(urlSend).success(function(d){
          //console.log(d);
          deferred.resolve(d);
         }).error(function(d){
            //console.log("error");
           ngNotify.set('Error deleting file.', {
              position:'top',
              type:'error',
              duration: 3000
             });

         });
        return deferred.promise;
      };
}]);
app.service('DataTables', ['$http','$q','ngNotify',
      function($http, $q, ngNotify){
        var deferred;
          this.getTable = function(id){
          var urlSend = base_domain+'/lectut_api/files/'+id+'/'; 
          deferred = $q.defer();
           $http.post(urlSend).success(function(d){
          //$http.get('http://beta.json-generator.com/api/json/get/FQlO35E').success(function (d) {
         // console.log(d);
          deferred.resolve(d);
          }).error(function(d){
            //console.log("error");
             ngNotify.set('Error getting files.', {
              position:'top',
              type:'error',
              duration: 3000
             });

          });
          return deferred.promise;
        };
}]);

app.service('Members', ['$http','$q','ngNotify',
      function($http, $q, ngNotify){
        var deferred;
          this.getMembers = function(id){
          var urlSend = base_domain+'/lectut_api/members/'+id+'/'; 
          deferred = $q.defer();
           $http.post(urlSend).success(function(d){  
          deferred.resolve(d);
          }).error(function(d){
             //console.log("error");
             ngNotify.set('Error fetching members.', {
              position:'top',
              type:'error',
              duration: 3000
             });
          });
          return deferred.promise;
        };
}]);

app.service('LoadFeed', ['$http','$q','ngNotify',
      function($http, $q, ngNotify){
        var deferred;
          this.loadFeed = function(id){
          var urlSend = base_domain+'/lectut_api/feeds/'+id+'/';
          //console.log(urlSend);
          deferred = $q.defer();
          $http.post(urlSend, {dataId: id}).success(function(d){
              deferred.resolve(d);
          }).error(function(d){
            //console.log("error");
             ngNotify.set('Error loading feed.', {
              position:'top',
              type:'error',
              duration: 3000
             });

          });
          return deferred.promise;
        };
}]);

app.service('LoadOnePost', ['$http','$q','ngNotify',
      function($http, $q, ngNotify){
        var deferred;
          this.getOnePost = function(courseId,postId){
          var urlSend = base_domain+'/lectut_api/feeds/'+courseId+'/'+ postId+'/';
          deferred = $q.defer();
          $http.post(urlSend).success(function(d){
              deferred.resolve(d);
          }).error(function(d){
            //console.log("error");
             ngNotify.set('Error loading post.', {
              position:'top',
              type:'error',
              duration: 3000
             });

          });
          return deferred.promise;
        };
}]);

app.service('LoadOneFile', ['$http','$q','ngNotify',
      function($http, $q,ngNotify){
        var deferred;
          this.getOneFile = function(courseId,fileId){
          var urlSend = base_domain+'/lectut_api/feeds/file/'+courseId+'/'+ fileId+'/';
          deferred = $q.defer();
          $http.post(urlSend).success(function(d){
              deferred.resolve(d);
          }).error(function(d){
            //console.log("error");
             ngNotify.set('Error loading file.', {
              position:'top',
              type:'error',
              duration: 3000
             });

          });
          return deferred.promise;
        };
}]);

app.service('SearchService', ['$http','$q','ngNotify',
      function($http, $q, ngNotify){
        var deferred;
          //console.log("s");
          this.getSearchData = function(qs){
          var urlSend = base_domain+'/lectut_api/search/?q='+qs;
          deferred = $q.defer();
          $http.post(urlSend).success(function(d){
              deferred.resolve(d);
          }).error(function(d){
            //console.log("error");
             ngNotify.set('Search failed.', {
              position:'top',
              type:'error',
              duration: 3000
             });
          });
          return deferred.promise;
        };
}]);
app.service('CourseDataById', ['$http','$q','ngNotify',
      function($http, $q, ngNotify){
        var deferred;
          //console.log("s");
          this.getCourseDataById = function(batchId){
          var urlSend = base_domain+'/lectut_api/batchDetails/'+batchId+'/';
          deferred = $q.defer();
          $http.post(urlSend).success(function(d){
              deferred.resolve(d);
          }).error(function(d){
            //console.log("error");
          });
          return deferred.promise;
        };
}]);

app.service('InitialSetup', ['$http','$q','ngNotify',
      function($http, $q, ngNotify){
        var deferred;
          //console.log("s");
          this.getInitialData = function(){
          var urlSend = base_domain+'/lectut_api/';
          deferred = $q.defer();
          $http.post(urlSend).success(function(d){
              deferred.resolve(d);
          }).error(function(d){
            //console.log("error");
            ngNotify.set('Connection refused. We are looking into it.', {
              position:'top',
              type:'error',
              duration: 200000
             });

          });
          return deferred.promise;
        };
}]);

app.service('Comments', ['$http','$q','ngNotify',
      function($http, $q, ngNotify){
        var deferred;
          //console.log("s");
          this.getComments = function(postId){
          var urlSend = base_domain+'/lectut_api/comments/'+postId+'/';
          deferred = $q.defer();
          $http.post(urlSend).success(function(d){
              deferred.resolve(d);
          }).error(function(d){
            //console.log("error");
             ngNotify.set('Error loading comment.', {
              position:'top',
              type:'error',
              duration: 3000
             });

          });
          return deferred.promise;
        };
}]);

app.service('LoadFacultyData', ['$http','$q','ngNotify',
      function($http, $q, ngNotify){
        var deferred;
          //console.log("s");
          this.getFacultyData = function(facultyId){
          var urlSend = base_domain+'/lectut_api/facultyFiles/'+facultyId+'/';
          deferred = $q.defer();
          $http.post(urlSend).success(function(d){
              deferred.resolve(d);
          }).error(function(d){
            //console.log("error");
             ngNotify.set('Error loading faculty profile.', {
              position:'top',
              type:'error',
              duration: 3000
             });

          });
          return deferred.promise;
        };
}]);


app.service('JoinCourse', ['$http','$q','ngNotify',
      function($http, $q, ngNotify){
        var deferred;
          //console.log("s");
          this.joinCourse = function(courseId){
          var urlSend = base_domain+'/lectut_api/joinBatch/'+courseId+'/';
          deferred = $q.defer();
          $http.post(urlSend).success(function(d){
              if(d.status === 100){
                deferred.resolve(d);
                ngNotify.set(d.msg, {
                  position:'top',
                  type:'success',
                  duration: 3000
                }); 
              }
              else{
                ngNotify.set(d.msg, {
                  position:'top',
                  type:'error',
                  duration: 3000
                }); 
              }
          }).error(function(d){
            //console.log("error");
             ngNotify.set('Cannot join this batch', {
              position:'top',
              type:'error',
              duration: 3000
             });

          });
          return deferred.promise;
        };
}]);

app.service('LeaveCourse', ['$http','$q','ngNotify',
      function($http, $q, ngNotify){
        var deferred;
          //console.log("s");
          this.leaveCourse = function(courseId){
          var urlSend = base_domain+'/lectut_api/leaveBatch/'+courseId+'/';
          deferred = $q.defer();
          $http.post(urlSend).success(function(d){
              if(d.status === 100){
                deferred.resolve(d);
                ngNotify.set(d.msg, {
                  position:'top',
                  type:'success',
                  duration: 3000
                }); 
              }
              else{
                ngNotify.set(d.msg, {
                  position:'top',
                  type:'error',
                  duration: 3000
                }); 
              }
          }).error(function(d){
            //console.log("error");
             ngNotify.set(d.msg, {
              position:'top',
              type:'error',
              duration: 3000
             });

          });
          return deferred.promise;
        };
}]);


app.factory('authHttpResponseInterceptor',['$q','$location',function($q,$location){
        return {
            // upto 300
            'response': function(response){
                if (response.data.lectut_status === 101) {
                    //for redirects to 404 
                    $location.path('/404');
                }
                return response || $q.when(response);
            },
            // above 300
            'responseError': function(rejection) {
              console.log(rejection);
                if (rejection.status === 401) {
                    console.log("401");
                } else if (rejection.status === 400) {
                   console.log("400");
                }
                return $q.reject(rejection);
            }
        }
    }])