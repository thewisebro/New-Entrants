'use strict';
var thing;
/**
 * @ngdoc function
 * @name lectutApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the lectutApp
 */
lectutApp
  .controller('MainCtrl', function ($scope) {

    //current user details
    $scope.userdetails = {
     username:'Himanshu Jariyal',
     enrollmentNo:"12114030",
     branch:"B.Tech CSE 3rd Year"  
    };
   
    $scope.users =[
    {
      url:"https://avatars2.githubusercontent.com/u/552817?v=3&s=80"
    },
    {
      url:"https://avatars0.githubusercontent.com/u/2171796?v=3&s=80"
    },
    {
      url:"https://avatars3.githubusercontent.com/u/810438?v=3&s=80"
    }
    ];
    //course name of current user
    $scope.courses = [
    {
      name:"Electronics and Communication",
      id:"EC-131",
      notifications:5
    },
    {
      name:"Physics",
      id:"PH-101",
      notifications:3
    }, 
    {
      name:"Business Managemnet",
      id:"BM-002",
      notifications:2
    }, 
    {
      name:"Fine arts and music",
      id:"FA-102",
      notifications:1
    },
    {
      name:"Hardware Lab",
      id:"EC-332",
      notifications:5
    }
    ];
  });


lectutApp.controller('CourseHomeCtrl', ['$routeParams', function($routeParams) {
  this.params = $routeParams;
}]);

lectutApp.controller('CourseDetailCtrl', ['$stateParams','$route','$scope','CourseDetails',function($stateParams,$route,$scope,CourseDetails) {
  this.params = $stateParams;
  $scope.courseId = this.params.courseId;
  $scope.courseName = "Physics and Chemistry";
 
  $scope.className = "red"; 
  $scope.changeClass = function(){
  
  }
   
  var promiseCourseData = CourseDetails.getCourseDetailsData();
  promiseCourseData.then(function (d) {
     //console.log(d);
     $scope.posts = d[0].posts;
     //console.log($scope.posts);  
  });
}]);

lectutApp.controller('CourseFeedsCtrl', ['$stateParams','$scope', function($stateParams,$scope) {

}]);

lectutApp.controller('CourseFilesCtrl', ['$stateParams', 'DataTables', 'DTOptionsBuilder' , 'DTColumnBuilder','DTInstances', '$scope', '$compile', function($stateParams, DataTables, DTOptionsBuilder, DTColumnBuilder, DTInstances,$scope, $compile) {
  this.params = $stateParams;
  var promiseCourseData = DataTables.getTable();
    
     var vm = this;
     vm.selected = {};
     vm.toggleAll = toggleAll;
   $scope.dtOptions = DTOptionsBuilder.fromFnPromise(promiseCourseData.then(
      function(d){
        return d;  
      }
   )  
   ).withOption('createdRow', function(row, data, dataIndex) {
                 // Recompiling so we can bind Angular directive to the DT
                             $compile(angular.element(row).contents())($scope);
                                     })
                          .withPaginationType('full_numbers');

     $scope.dtColumns = [
             DTColumnBuilder.newColumn(null).withTitle('').notSortable()
                        .renderWith(function(data, type, full, meta) {
                                      return '<input type="checkbox" ng-model="showCase.selected[' + data.id + ']">';
                        }),
             DTColumnBuilder.newColumn('id').withTitle('ID'),
             DTColumnBuilder.newColumn('fileName').withTitle('Name'),
             DTColumnBuilder.newColumn('postedBy').withTitle('Posted By'), 
             DTColumnBuilder.newColumn('fileType').withTitle('Type'),
             DTColumnBuilder.newColumn('postedOn').withTitle('Date'),
     ];
      
      
     DTInstances.getLast().then(function (dtInstance) {
               dtInstance.DataTable.data().each(function(data) {
                     vm.selected[data.id] = false;
               });
      });
     
         var _toggle = true;
         function toggleAll() {
           console.log("s");
            for (var prop in vm.selected) {
              console.log("as");
               if (vm.selected.hasOwnProperty(prop)) {
                     vm.selected[prop] = _toggle;
               }
            }
            _toggle = !_toggle;
          }                        

}]);


lectutApp.controller('CourseMembersCtrl', ['$stateParams', function($stateParams) {
  this.params = $stateParams;
}]);
