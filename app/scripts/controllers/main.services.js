'use strict';

var app = angular.module('lectutApp');
app.service('CourseDetails', ['$http', '$q',
      function ($http, $q) {
        var deferred = $q.defer();
        $http.get('http://beta.json-generator.com/api/json/get/PVV9-On').then(function (d) {
        deferred.resolve(d);
      });
      this.getCourseDetailsData = function () {
        return deferred.promise;
      };
}]);
