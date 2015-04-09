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
  .controller('MainCtrl', ['$scope','$routeParams','$rootScope','SearchService', 'InitialSetup','CourseDetails',function ($scope, $routeParams, $rootScope, SearchService, InitialSetup, CourseDetails) {
    
    $rootScope.whichView = "MainCtrl";
    $scope.base_media_url = base_domain+"/media/";
    $scope.base_domain = base_domain;

    //------------------ Initial setup-------------------------------------
    $scope.logIn = false;
    $scope.auth;
    //console.log("This is start ----- lectut");
    var promiseInitialSetup = InitialSetup.getInitialData();
    promiseInitialSetup.then(function(d){
         // console.log(d);
         console.log(d);
         $scope.auth = d;
         $rootScope.commonPosts = d.posts;
         console.log("this is auth");
         //console.log($scope.auth.userType == "2");
         if($scope.auth.userType == "0" || $scope.auth.userType == "1"){
            $scope.logIn = true;
            for(var i=0;i<$scope.auth.batches.length;i++){
              if($scope.auth.batches[i].id == $scope.courseId.courseId){
                $scope.courseName = $scope.auth.batches[i].course_name;
                $scope.courseCode = $scope.auth.batches[i].code;
              }
            }
        }
        else{
          //anon user
          console.log("-------------------anon--------------------");
          $scope.logIn = false;
        }
    });
    
    // To get feed data.
    var x  = $routeParams;
    $scope.courseId = x;
    
    // Initially setting the selected Course
    console.log("--------------------------------------------");
    $scope.selectedCourse = x.courseId;


    // Search Global
   $scope.queryString = "";
   $scope.searchFunc = function(str){
    //alert("sad");
    console.log(str);
    if(str){
    var searchData = SearchService.getSearchData(str);
    searchData.then(function (d) {
       $scope.searchResults = d;
       console.log(d);
    });
    }
    }

   $scope.clearSearch = function(){
    $scope.searchResults = "";
    $scope.queryString="";
    $scope.searchFunc("");
   }
   

   $scope.getFeedData = function(id){
    //console.log("asdsad");
    $scope.selectedCourse=id;
        for(var i=0;i<$scope.auth.batches.length;i++){
          if($scope.auth.batches[i].id == id){
            $scope.courseName = $scope.auth.batches[i].course_name;
          }
        }
    var promiseCourseData = CourseDetails.getCourseDetailsData(id);

    promiseCourseData.then(function (d) {
       $scope.posts = d.posts;
       console.log(d);
    });
  }



  }]);


lectutApp.controller('CourseHomeCtrl', ['$routeParams','$scope','$rootScope','RemoveFeedPost','RemoveFeedFile', 'Comments',function($routeParams, $scope,$rootScope, RemoveFeedPost, RemoveFeedFile, Comments) {
  //this.params = $routeParams;
   
   $rootScope.whichView = "CourseHomeCtrl";  
  // ------------------------- Comments -----------------------
  $scope.loadCommentsFunc = function(id){
    var promiseComments = Comments.getComments(id);
          promiseComments.then(function(x){
          console.log("-------------------");
          console.log(id);
          $('#postComments_'+id).append(x);
    });
  }


  $scope.removeFeedPost = function(id, index){
    console.log("This is to be deleted.. "+id);
    console.log($scope.posts);

    sweetAlert({
        title: "Are you sure?",
        text: "Your will not be able to recover this feed post!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false,
        closeOnCancel: false
        },
        function(isConfirm){
          if(isConfirm){
            var promiseRemoveFeedPost = RemoveFeedPost.deleteFeedPost(id);
            promiseRemoveFeedPost.then(function(d){
              console.log("Deleted this man"+ id);
              $rootScope.commonPosts.splice(index,1);
              sweetAlert("Deleted!", "Post has been deleted.", "success");
            },
            function(reason){
              sweetAlert("Deleted!", reason, "success");
            }
            );
          }
          else{
              sweetAlert("Cancelled!", "Post is not deleted.", "error");
          }
    });
}

 $scope.removeFeedFile = function(id, parentIndex, index){
    console.log("This is to be deleted.. "+id);
    console.log($scope.posts);

    sweetAlert({
        title: "Are you sure?",
        text: "Your will not be able to recover this file!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false,
        closeOnCancel: false
        },
        function(isConfirm){ 
             if(isConfirm){
               var promiseRemoveFeedFile = RemoveFeedFile.deleteFeedFile(id);
               promiseRemoveFeedFile.then(function(d){
                 console.log("Deleted this file man"+ id);
                 $rootScope.commonPosts[parentIndex].files.splice(index,1);
                 sweetAlert("Deleted!", "File has been deleted.", "success");
               },
               function(reason){
                 sweetAlert("Cancelled!", reason, "error");
               }
              );
             }
             else{
                 sweetAlert("Cancelled!", "File is not deleted.", "error");
             } 
   });
 }


}]);

lectutApp.controller('CourseDetailCtrl', ['$scope','CourseDetails','FeedFileDownload', 'RemoveFeedPost','RemoveFeedFile','$cookies','$upload','$timeout','$routeParams','LoadFeed','growl','Comments','$rootScope',function($scope,CourseDetails,FeedFileDownload, RemoveFeedPost , RemoveFeedFile,$cookies,$upload, $timeout, $routeParams,LoadFeed, growl, Comments,$rootScope) {
   
   $rootScope.whichView = "CourseDetailCtrl";
   this.params = $routeParams;
   var csrf = $cookies.csrftoken;
   var y = $routeParams;
   $scope.coId = y;

   $scope.uploadItems = [
      'Lecture',
      'Tutorial',
      'ExamPaper',
      'Solution'
   ];

    $scope.toggled = false;

    $scope.changeToggle = function(){
       if($scope.toggled){
          $timeout(function(){
           $scope.toggled = false;
          },10);
        }
        else{
        $timeout(function(){
           $scope.toggled = true;
          },10);
        }
        console.log($scope.toggled);
    }
    
    angular.element(document).on('click', function(e){ 
        if(e.target.className != "fourChoice"){
           $scope.toggled? $scope.changeToggle() : "";
        }
    });
/*
    $scope.$watch(
      function($scope) { 
        return $scope.toggled;
      },
      function($scope){
        alert("s");
        if($scope.toggled){
          $timeout(function(){
           $scope.toggled = false;
          },0);
        }
        else{
        $timeout(function(){
           $scope.toggled = true;
          },0);
        }
    }
    );
  */  
  //--------------------------------------- NEW POST-----------------------------------
  /*$scope.$watch('files', function () {
          $scope.upload($scope.files);
  });*/
  $scope.fileArray={
    Lecture : [],
    Tutorial: [],
    ExamPaper: [],
    Solution: []
  };

  var upload = function (myfiles,typeArray,content){
    $upload.upload({
      url: base_domain+'/lectut_api/upload/'+$routeParams.courseId+'/', // upload.php script, node.js route, or servlet url
      file: myfiles,  // single file or an array of files (array is for html6 only)
      method: 'POST',
      headers: {'Content-Type':'multipart/form-data'}, // only for html5
      //fileName: 'doc.jpg' or ['1.jpg', '2.jpg', ...], // to modify the name of the file(s)
      /*
         file formData name ('Content-Disposition'), server side request form name could be
         an array  of names for multiple files (html5). Default is 'file' */
      //fileFormDataName: fileType, //array of files.
      /*
         map of extra form data fields to send along with file. each field will be sent as a form field.
         The values are converted to json string or jsob blob depending on 'sendObjectsAsJsonBlob' option. */
      //fields: {key: $scope.myValue, ...},
      /*
         if the value of a form field is an object it will be sent as 'application/json' blob 
         rather than json string, default false. */
     // sendObjectsAsJsonBlob: true|false,
      /* customize how data is added to the formData. See #40#issuecomment-28612000 for sample code. */
      //formDataAppender: function(formData, key, val){},
      /*
         data will be sent as a separate form data field called "data". It will be converted to json string 
         or jsob blob depending on 'sendObjectsAsJsonBlob' option*/
      data: {
        user: "harshithere",
        formText: content,
        typeData: typeArray,
        privacy: !$scope.privacy
      },
      withCredentials: true,
      //and all other angular $http() options could be used here.
  }).progress(function (evt) {
            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
            console.log('progress: ' + progressPercentage + '% ' +
            evt.config.file.name);
        }).success(function (data, status, headers, config) {
            console.log('file ' + config.file.name + 'uploaded. Response: ' +
            JSON.stringify(data));
            console.log("data");
            var result = JSON.stringify(data);
            //console.log($scope.posts);
            $scope.posts.unshift(data);

            // null the top box 
            $scope.thing.content = "";
            $scope.fileArray={
               Lecture : [],
               Tutorial: [],
               ExamPaper: [],
               Solution: []
             };
          // Notifiaction Success
             console.log("growl below");
          growl.addSuccessMessage("This adds a success message");
        });

  }
/* then promise (note that returned promise doesn't have progress, xhr and cancel functions. */
//var promise = upload.then();


//----------------------------------------------------------------------------------

  $scope.update = function(files,type){
     $scope.fileArray[type] = $scope.fileArray[type].concat(files);
     console.log(files);
  }

  $scope.thing = {'content':'','data':''};
  $scope.finalSend = function(){
         
         var things =  [];

         var typeData = [];
         var temp = $scope.fileArray.Lecture.length;
         while(temp--){
            typeData.push("lec");
         }
         temp = $scope.fileArray.Tutorial.length;
         while(temp--){
            typeData.push("tut");
         }
         temp = $scope.fileArray.ExamPaper.length;
         while(temp--){
            typeData.push("exp");
         }
         temp = $scope.fileArray.Solution.length;
         while(temp--){
            typeData.push("sol");
         }
         var myfile = $scope.fileArray;
          things = things.concat(myfile.Lecture);
          things = things.concat(myfile.Tutorial);
          things = things.concat(myfile.ExamPaper);
          things = things.concat(myfile.Solution);

          console.log("Things dajlksdjsa ld");
          console.log(things);
          console.log(!$scope.privacy);
          upload(things,typeData,$scope.thing.content);
          //console.log("----------------");
          console.log(typeData);
  }

  $scope.deleteItem = function(item, type){
              //console.log(type);
        $scope.fileArray[type].splice(item,1);
        console.log($scope.fileArray[type]);
  }
 

  // ------------------------- Comments -----------------------
  $scope.loadCommentsFunc = function(id){
    var promiseComments = Comments.getComments(id);
          promiseComments.then(function(x){
          console.log("-------------------");
          console.log(id);
          $('#postComments_'+id).append(x);
    });
  }

  //-------------------------- Posts---------------------------
  // Loads the feed automatically on reload on a specific url.
  // check http://172.25.55.156:9008/course/3/feeds : feeds will be loaded.
  $scope.courseId = this.params.courseId;
  //$scope.courseName = "Physics and Chemistry";

  var promiseCourseData = CourseDetails.getCourseDetailsData($scope.courseId);

    promiseCourseData.then(function (d) {
       $scope.posts = d.posts;
       console.log(d);
    });

  $scope.getFeedData = function(id){
    //console.log("asdsad");
    var promiseCourseData = CourseDetails.getCourseDetailsData(id);

    promiseCourseData.then(function (d) {
       $scope.posts = d.posts;
       console.log(d);
    });
  }
  
  $scope.downloadFeedFile = function(id){
    growl.addSuccessMessage("This adds a success message");
    console.log("herecomesid");
    console.log(id);
    var promiseFeedFileDownload = FeedFileDownload.getFeedFile(id);
    promiseFeedFileDownload.then(function(d){
         console.log("gai aur ayi downl rq");
          var blob = new Blob([d], {type: "image/jpeg"});
              var objectUrl = URL.createObjectURL(blob);
                  window.open(objectUrl);
    });
  }

  $scope.removeFeedPost = function(id, index){
    console.log("This is to be deleted.. "+id);
    console.log($scope.posts);

    sweetAlert({
        title: "Are you sure?",
        text: "Your will not be able to recover this feed post!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false,
        closeOnCancel: false
        },
        function(isConfirm){
          if(isConfirm){
            var promiseRemoveFeedPost = RemoveFeedPost.deleteFeedPost(id);
            promiseRemoveFeedPost.then(function(d){
              console.log("Deleted this man"+ id);
              $scope.posts.splice(index,1);
              sweetAlert("Deleted!", "Post has been deleted.", "success");
            },
            function(reason){
              sweetAlert("Deleted!", reason, "success");
            }
            );
          }
          else{
              sweetAlert("Cancelled!", "Post is not deleted.", "error");
          }
    });
}

 $scope.removeFeedFile = function(id, parentIndex, index){
    console.log("This is to be deleted.. "+id);
    console.log($scope.posts);

    sweetAlert({
        title: "Are you sure?",
        text: "Your will not be able to recover this file!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false,
        closeOnCancel: false
        },
        function(isConfirm){ 
             if(isConfirm){
               var promiseRemoveFeedFile = RemoveFeedFile.deleteFeedFile(id);
               promiseRemoveFeedFile.then(function(d){
                 console.log("Deleted this file man"+ id);
                 $scope.posts[parentIndex].files.splice(index,1);
                 sweetAlert("Deleted!", "File has been deleted.", "success");
               },
               function(reason){
                 sweetAlert("Cancelled!", reason, "error");
               }
              );
             }
             else{
                 sweetAlert("Cancelled!", "File is not deleted.", "error");
             } 
   });
 }
  /*$scope.feedLoaded = 0;
  $scope.myPagingFunction = function(){
    var promiseRemoveFeedFile = LoadFeed.loadFeed($scope.feedLoaded);
    promiseRemoveFeedFile.then(function(d){
      var a=[],b=[];
      b = a.concat(d.data.posts);
      $scope.posts = b;
      console.log(d.data.posts);
      console.log($scope.posts);
      $scope.feedLoaded = $scope.feedLoaded + 1;
    });
 }
*/



/* ---------------------------------------------------------------------
    Growl Notifications
----------------------------------------------------------------------*/
/*  growl.addWarnMessage("This adds a warn message");
    growl.addInfoMessage("This adds a info message");
    growl.addSuccessMessage("This adds a success message");
    growl.addErrorMessage("This adds a error message");
*/

}]);

lectutApp.controller('CourseFeedsCtrl', ['$stateParams','$scope', function($stateParams,$scope) {

}]);

lectutApp.controller('CourseFilesCtrl', [ 'DataTables', 'DTOptionsBuilder' , 'DTColumnBuilder','DTInstances', '$scope', '$compile', '$routeParams','$rootScope',function( DataTables, DTOptionsBuilder, DTColumnBuilder, DTInstances,$scope, $compile, $routeParams, $rootScope) {
   console.log("++++++++++++++++Course Files Ctrl+++++++++++++++");
    var promiseCourseData = DataTables.getTable($routeParams.courseId);
  $rootScope.whichView = "CourseFilesCtrl";
   $scope.selected = {};
   
   $scope.dtOptions = DTOptionsBuilder.fromFnPromise(
     promiseCourseData.then(
      function(d){
        console.log(d);
        var allFiles = [];
        allFiles = allFiles.concat(d.archiveFiles.tut);
        allFiles = allFiles.concat(d.archiveFiles.lec);
        allFiles = allFiles.concat(d.archiveFiles.exp);
        allFiles = allFiles.concat(d.archiveFiles.sol);
        allFiles = allFiles.concat(d.archiveFiles.que);
        allFiles = allFiles.concat(d.currentFiles.tut);
        allFiles = allFiles.concat(d.currentFiles.lec);
        allFiles = allFiles.concat(d.currentFiles.exp);
        allFiles = allFiles.concat(d.currentFiles.sol);
        allFiles = allFiles.concat(d.currentFiles.que);
        return allFiles;
      }
   )
   ).withOption('createdRow', function(row, data, dataIndex) {
                 // Recompiling so we can bind Angular directive to the DT
                 $compile(angular.element(row).contents())($scope);
    }).withOption('paging',false).withOption('compact','true');
    //.withPaginationType('full_numbers');
 
    $scope.dtColumns = [
             /*DTColumnBuilder.newColumn(null).withTitle('<div type="checkbox">Mark</div>').notSortable()
                 .renderWith(function(data, type, full, meta) {
                 return '<input type="checkbox" ng-change="toggleOne('+ data.id+')" ng-checked="selected['+data.id+']" ng-model="$scope.selected[' + data.id + ']">';
             }),*/
             // DTColumnBuilder.newColumn('id').withTitle('ID'),
             DTColumnBuilder.newColumn(null).withTitle('<span>Name</span>')
             .renderWith(function(data,type,full){
                 //console.log(full.file_type);
                 var html= "";
                 //html += '<input type="checkbox" style="margin-right:10px;margin-left:5px;" ng-change="toggleOne('+ data.id+')" ng-checked="selected['+data.id+']" ng-model="$scope.selected[' + data.id + ']">';
                 if(full.file_type == "unknown"){
                   html += '<i class="fa fa-file" style="margin-right:10px; font-size:16px;"></i><span>'+full.description+'</span>';
                 }
                 else{
                   html += '<i class="fa fa-file-'+ full.file_type +'-o" style="margin-right:10px; font-size:16px;"></i><span>'+full.description+'</span>';
                }
                html += '<span class="fileShowUser">by: '+full.username+'</span>';
                html += '<span class="fileShowDownloads">Downloads: '+2+'</span>';
                return html;
             }),
            // DTColumnBuilder.newColumn('description').withTitle('Name'),
             DTColumnBuilder.newColumn('upload_type').withTitle('Type').notSortable().notVisible(),
             DTColumnBuilder.newColumn('datetime_created').withTitle('Share Date')
             .renderWith(function(data, type, full, meta) {
                 //console.log(data);
                 var html = "";
                 html += '<div style=" display: inline-block;"><span class="timeFile">'+ moment(data).format("DD-MM-YY, HH:mm");+'</span></div>';
                 html += '<div style="display: inline-block; margin-left:30px;"><i class="fa fa-cog fileSetting" ng-click="toggleAll()"></i></div>';
                 return html;
             })/*
             DTColumnBuilder.newColumn(null).withTitle('').notSortable()
             .renderWith(function(data, type, full, meta) {
                 //return '<div class="downloadFile" ng-click="toggleAll()">Download</div>';
                 return '<i class="fa fa-cog fileSetting" ng-click="toggleAll()"></i>';
             })*/
      ];
        DTInstances.getLast().then(function (dtInstance) {
          dtInstance.DataTable.data().each(function(data) {
               $scope.selected[data.id] = false;
          });
          /*
          var id = '#' + "DataTables_Table_0";
          console.log(id);

          // Code to make individual header search.
          
          $(id + ' thead th').each(function() {
            var title = $(id + ' thead th').eq($(this).index()).text();
            $(this).html('<input type="text" placeholder="Search ' + title + '" />');
          });

          var table = $("#DataTables_Table_0").DataTable();
          // Apply the search
          table.columns().eq(0).each(function(colIdx) {
            $('input', table.column(colIdx).header()).on('keyup change', function() {
              table
              .column(colIdx)
              .search(this.value)
              .draw();
              });
            });
          */
         var table = $("#DataTables_Table_0").DataTable();
         //table.column(0).visible('false'); 
         table.columns().indexes().flatten().each( function ( i ) {
             if(i==1){
             var column = table.column( i );
             var select = $('<select id="fileFilterType"><option value=""></option></select>')
             .appendTo( $("#DataTables_Table_0_wrapper") )
             .on( 'change', function () {
               var val = $.fn.dataTable.util.escapeRegex(
                 $(this).val()
                 );

               column
               .search( val ? '^'+val+'$' : '', true, false )
               .draw();
               } );

             column.data().unique().sort().each( function ( d, j ) {
               select.append( '<option value="'+d+'">'+d+'</option>' )
               } );
         } });


     });


 

         // Table Upload Type implementation

         var table = $("#DataTables_Table_0").DataTable();
         console.log("_+_+_+_+_+_+");
         if(table){
            console.log("_________________________________");
         }
         console.log(table);
         //table.column(0).visible('false'); 
         table.columns().indexes().flatten().each( function ( i ) {
             if(i==1){
             var column = table.column( i );
             var select = $('<select id="fileFilterType"><option value=""></option></select>')
             .appendTo( $("#DataTables_Table_0_wrapper") )
             .on( 'change', function () {
               var val = $.fn.dataTable.util.escapeRegex(
                 $(this).val()
                 );

               column
               .search( val ? '^'+val+'$' : '', true, false )
               .draw();
               } );

             column.data().unique().sort().each( function ( d, j ) {
               select.append( '<option value="'+d+'">'+d+'</option>' )
               } );
         } });
      // ------------------------------
    
         //console.log("err1");
     var _toggle = true;
     $scope.toggleAll = function(){
       //console.log("asd");
        // console.log($scope.selected);
         for (var prop in $scope.selected) {
          // console.log($scope.selected[prop]);
            if ($scope.selected[prop]) {
              $scope.selected[prop] = false;
            }
            else{
              $scope.selected[prop]= true;
            }
         }
        // console.log($scope.selected);
     }

     $scope.toggleOne = function(id){
      //console.log(id);
      if($scope.selected[id]){
        $scope.selected[id] = false;
      }
      else{
        $scope.selected[id] = true;
      }
     }

     $scope.selectAll = function(id){
         for (var prop in $scope.selected) {
              $scope.selected[prop] = true;
         }
     }

}]);


lectutApp.controller('CourseMembersCtrl', ['Members','$scope','$routeParams', '$rootScope',function(Members, $scope, $routeParams, $rootScope) {
    //var batId;
    $rootScope.whichView = "CourseMembersCtrl";
    var promiseMembers = Members.getMembers($routeParams.courseId);
    promiseMembers.then(function(d){
      $scope.members = d;
      console.log(d);
    });
}]);


lectutApp.controller('CourseOnePostCtrl', ['LoadOnePost','$scope','$routeParams','FeedFileDownload','RemoveFeedPost' ,'RemoveFeedFile','Comments', '$rootScope',function(LoadOnePost, $scope, $routeParams, FeedFileDownload, RemoveFeedPost, RemoveFeedFile, Comments, $rootScope) {
    //console.log($routeParams);
    $rootScope.whichView = "CourseOnePostCtrl";
    var promiseMembers = LoadOnePost.getOnePost($routeParams.courseId,$routeParams.postId);
    promiseMembers.then(function(d){
      $scope.onePost = d.post;
      console.log(d);
    });

  // ------------------------- Comments -----------------------
  $scope.loadCommentsFunc = function(id){
    var promiseComments = Comments.getComments(id);
          promiseComments.then(function(x){
          console.log("-------------------");
          console.log(id);
          $('#postComments_'+id).append(x);
    });
  }
 
  $scope.removeFeedPost = function(id, index){
    console.log("This is to be deleted.. "+id);
    console.log($scope.onePost);

    sweetAlert({
        title: "Are you sure?",
        text: "Your will not be able to recover this feed post!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false,
        closeOnCancel: false
        },
        function(isConfirm){
          if(isConfirm){
            var promiseRemoveFeedPost = RemoveFeedPost.deleteFeedPost(id);
            promiseRemoveFeedPost.then(function(d){
              console.log("Deleted this man"+ id);
              console.log($scope.onePost);
              $scope.onePost={};
              sweetAlert("Deleted!", "Post has been deleted.", "success");
            },
            function(reason){
              sweetAlert("Deleted!", reason, "success");
            }
            );
          }
          else{
              sweetAlert("Cancelled!", "Post is not deleted.", "error");
          }
    });
}

 $scope.removeFeedFile = function(id, parentIndex, index){
    console.log("This is to be deleted.. "+id);
    
    sweetAlert({
        title: "Are you sure?",
        text: "Your will not be able to recover this file!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false,
        closeOnCancel: false
        },
        function(isConfirm){ 
             if(isConfirm){
               var promiseRemoveFeedFile = RemoveFeedFile.deleteFeedFile(id);
               promiseRemoveFeedFile.then(function(d){
                 console.log("Deleted this file man"+ id);
                 $scope.onePost.files.splice(index,1);
                 sweetAlert("Deleted!", "File has been deleted.", "success");
                 console.log(d);
               },
               function(reason){
                 sweetAlert("Cancelled!", reason, "error");
               }
              );
             }
             else{
                 sweetAlert("Cancelled!", "File is not deleted.", "error");
             } 
   });
 }

}]);

lectutApp.controller('CourseOneFileCtrl', ['LoadOneFile','$scope','$routeParams','FeedFileDownload','RemoveFeedFile','$rootScope',function(LoadOneFile, $scope, $routeParams, FeedFileDownload, RemoveFeedFile, $rootScope) {
    console.log($routeParams);
    $rootScope.whichView = "CourseOneFileCtrl";
    var promiseMembers = LoadOneFile.getOneFile($routeParams.courseId,$routeParams.fileId);
    promiseMembers.then(function(d){
      $scope.oneFile = d;
      console.log(d);
    });

   $scope.removeFeedFile = function(id, parentIndex, index){
    console.log("This is to be deleted.. "+id);

    sweetAlert({
        title: "Are you sure?",
        text: "Your will not be able to recover this file!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false,
        closeOnCancel: false
        },
        function(isConfirm){ 
             if(isConfirm){
               var promiseRemoveFeedFile = RemoveFeedFile.deleteFeedFile(id);
               promiseRemoveFeedFile.then(function(d){
                 console.log("Deleted this file man"+ id);
                 $scope.oneFile.files.splice(index,1);
                 sweetAlert("Deleted!", "File has been deleted.", "success");
                 console.log(d);
               },
               function(reason){
                 sweetAlert("Cancelled!", reason, "error");
               }
              );
             }
             else{
                 sweetAlert("Cancelled!", "File is not deleted.", "error");
             } 
   });
 }

}]);
