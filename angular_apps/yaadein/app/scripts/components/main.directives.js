'use strict';

var app = angular.module('yaadeinApp');

app.directive('showFocus', function($timeout) {
  return function(scope, element, attrs) {
    scope.$watch(attrs.showFocus, 
      function (newValue) { 
        $timeout(function() {
            element[0].focus();
        });
      }, true);
  };    
});
