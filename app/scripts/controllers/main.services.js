'use strict';

var app = angular.module('lectutApp');
app.service('CourseDetails', ['$http', '$q',
      function ($http, $q) {
       var deferred; 
       this.getCourseDetailsData = function () {
         deferred = $q.defer();
         $http.get('http://beta.json-generator.com/api/json/get/PVV9-On').success(function (d) {
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
          this.getTable = function(){
          deferred = $q.defer();
          $http.get('http://beta.json-generator.com/api/json/get/FQlO35E').success(function (d) {
         // console.log(d);
          deferred.resolve(d);
          }).error(function(d){
            console.log("error");
          });
          return deferred.promise;
        };        
}]);

