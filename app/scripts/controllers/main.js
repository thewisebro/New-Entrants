'use strict';

/**
 * @ngdoc function
 * @name lectutApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the lectutApp
 */
angular.module('lectutApp')
  .controller('MainCtrl', function ($scope) {

    //current user details
    $scope.userdetails = {
     username:"Himanshu Jariyal",
     enrollmentNo:"12114030",
     branch:"CSE"  
    };
   
    //course name of current user
    $scope.courses = [
    {
      name:"Electronics and Communication",
      id:"EC-101"
    },
    {
      name:"Physics",
      id:"CC-301"
    }, 
    {
      name:"Business Managemnet",
      id:"ME-401"
    }, 
    {
      name:"Fine arts and music",
      id:"REC-101"
    },
    {
      name:"Hardware Lab",
      id:"WE-161"
    }
    ];
  });

