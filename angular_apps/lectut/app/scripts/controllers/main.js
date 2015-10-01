  'use strict';
  var thing;
  /**
   * @ngdoc function
   * @name lectutApp.controller:MainCtrl
   * @description
   * # MainCtrl
   * Controller of the lectutApp
   */

  var redirect_url = base_domain + '/login/?next=/lectut/';
lectutApp.controller('MainCtrl', ['$location','$scope','$routeParams','$rootScope','SearchService', 'InitialSetup','CourseDetails','CourseDataById','ngNotify','JoinCourse','LeaveCourse',function ($location,$scope, $routeParams, $rootScope, SearchService, InitialSetup, CourseDetails, CourseDataById, ngNotify,JoinCourse, LeaveCourse) {

    // New custom theme in notification
    ngNotify.addType('myTheme', 'notiLec');
     ngNotify.config({
       theme: 'myTheme'
    });

    // Root scope for link highlighting
    $rootScope.whichView = "MainCtrl";
    $scope.base_media_url = base_domain+"/media/";
    $scope.base_domain = base_domain;
 
    // To get feed data.
    $scope.courseId = $routeParams;
    $scope.updateCourseId = function(id){
          var promiseCourseDataById = CourseDataById.getCourseDataById(id);
          promiseCourseDataById.then(function(d){
            //console.log("-----------------------");
            //console.log(d);
            //alert(d.batch);
            //console.log(d);
            $scope.courseName = d.batch_info.course_name;
            $scope.courseCode = d.batch_info.code;
            $scope.courseid = id;
            $scope.teaching = false;
            if($scope.auth && $scope.auth.batches){
              for(var i=0;i<$scope.auth.batches.length;i++){
                if($scope.auth.batches[i].id == id){
                 $scope.teaching = true;
                }
              }  
            }
          });
    }

    function updateCourseName(){
      if($routeParams.courseId){
         //console.log($routeParams.courseId);
         $scope.updateCourseId($routeParams.courseId);
      }
      else{
        //console.log("asd");
        if( $rootScope.whichView != "CourseHomeCtrl"){
          setTimeout(function(){ updateCourseName(); }, 100);
        }
      }
    }
  
    updateCourseName();

    //$scope.updateCourseId($routeParams.courseId);
    $scope.selectedCourse = $routeParams.courseId;
   // console.log($scope.courseId);
    
    // Check if a particular link is active
    // Is active
     $scope.isActive = function(route) {
        return route === $location.path().substring(0,route.length-1) +"/";
     }
    // Is active filter
     $scope.isActiveTab = function(route) {
       var routeB = route.split("").reverse().join("");
       var pathB =  $location.path().split("").reverse().join("");
       var check =false;
       var i=0;
       while(pathB[i] != "/" || routeB[i] != "/"){
          if(pathB[i] != routeB[i]){ 
            return false;
          }
          i++;
          if(i>30){
            return false;
          }
       }
       if(pathB[i]==routeB[i]){
        return true;
       }
       else{
        return false;
       }
    }
    
    // Check if url is Home i.e /#/ 
    $scope.isHome = function(route){
       return route === $location.path();
    }

    // ------------------- Sign Up --------------------
    $scope.signUp = function(){
      //console.log($scope.logIn);
       if ($scope.logIn === false) {
           window.location = redirect_url;
       }
       else{
        //alert("asd");
       }
    }

    //------------------ Initial setup-------------------------------------
    $scope.logIn = false;
    $scope.auth;
    //console.log("This is start ----- lectut");
    var promiseInitialSetup = InitialSetup.getInitialData();
    promiseInitialSetup.then(function(d){
         // console.log(d);
         //console.log(d);
         $scope.auth = d;
         $rootScope.commonPosts = d.posts;

         console.log("jome");
         console.log($rootScope.commonPosts);
         //console.log("this is auth");
         //console.log($scope.auth.userType == "2");
         if($scope.auth.userType == "0" || $scope.auth.userType == "1"){
            $scope.logIn = true;
            for(var i=0;i<$scope.auth.batches.length;i++){
              if($scope.auth.batches[i].id == $scope.courseId.courseId){
                $scope.courseName = $scope.auth.batches[i].course_name;
                $scope.courseCode = $scope.auth.batches[i].code;
                $scope.courseid= $scope.courseId.courseId;
              }
            }
        }
        else{
          //anon user
          //console.log("-------------------anon--------------------");
          $scope.logIn = false;
          
          var promiseCourseDataById = CourseDataById.getCourseDataById($routeParams.courseId);
          promiseCourseDataById.then(function(d){
            //console.log(d);
            $scope.courseName = d.course_name;
            $scope.courseCode = d.code;
            $scope.courseid= $routeParams.courseId;
          });
        }
        //$("body").show();
        $(".bodyOverlay").hide();
    });
   
   // Search Global
   $scope.queryString = "";
   $scope.searchFunc = function(str){
    //console.log(str);
    if(str){
      var searchData = SearchService.getSearchData(str);
      searchData.then(function (d) {
         $scope.searchResults = d;
         //console.log(d);
      });
     }
    }

   $scope.clearSearch = function(){
    $scope.searchResults = "";
    $scope.queryString="";
    $scope.searchFunc("");
   }
  
   $scope.getFeedData = function(id){
    $scope.selectedCourse=id;
        if($scope.auth.userType == "1"){
          for(var i=0;i<$scope.auth.batches.length;i++){
            if($scope.auth.batches[i].id == id){
              $scope.courseName = $scope.auth.batches[i].course_name;
              $scope.courseid = id;
            }
          }  
        }
    var promiseCourseData = CourseDetails.getCourseDetailsData(id);

    promiseCourseData.then(function (d) {
       $scope.posts = d.posts;
       $scope.is_member = d.in_batch;
       console.log("asdsadsad");
    });
  }

  $scope.isCourseCheck = function(){
    
  }

  $scope.getPostData = function(courseId) {
    
  }

  $scope.joinCourse = function(id){
    var promiseJoinCourse = JoinCourse.joinCourse(id);
    promiseJoinCourse.then(function(d){
      if(d.status === 100){
        $scope.teaching = true;  
      }
    });
  }

   $scope.leaveCourse = function(id){
    var promiseLeaveCourse = LeaveCourse.leaveCourse(id);
    promiseLeaveCourse.then(function(d){
      if(d.status === 100){
        $scope.teaching = false;  
      }
    });
  }

}]);


lectutApp.controller('CourseHomeCtrl', ['$routeParams','$scope','$rootScope','RemoveFeedPost','RemoveFeedFile', 'Comments',function($routeParams, $scope,$rootScope, RemoveFeedPost, RemoveFeedFile, Comments) {
  //this.params = $routeParams;
  $rootScope.whichView = "CourseHomeCtrl";  
  
  // ------------------------- Comments -----------------------
  $scope.loadCommentsFunc = function(id){
   if($('#postComments_'+id).hasClass("open")){
        $('#postComments_'+id).removeClass("open");
        $('#postComments_'+id).html("");
    }
    else{
      $('#postComments_'+id).addClass("open");
      var promiseComments = Comments.getComments(id);
            promiseComments.then(function(x){
            //console.log("------Course Home Co-----------");
            //console.log(id);
            $('#postComments_'+id).append(x);
      });
    }
  }


  $scope.removeFeedPost = function(id, index){
    //console.log("This is to be deleted.. "+id);
    //console.log($scope.posts);

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
              //console.log("Deleted this man"+ id);
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
    //console.log("This is to be deleted.. "+id);
    //console.log($scope.posts);
    //common
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
                 //console.log("Deleted this file man"+ id);
                 $rootScope.commonPosts[parentIndex].files.splice(index,1);
                 sweetAlert("Deleted!", "File has been deleted.", "success");
                 //alert("sd");
                 if($rootScope.commonPosts[parentIndex].files.length == 0 && $rootScope.commonPosts[parentIndex].post.content == ""){
                      $rootScope.commonPosts.splice(parentIndex,1)
                 }

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

lectutApp.controller('CourseDetailCtrl', ['$scope','CourseDetails','FeedFileDownload', 'RemoveFeedPost','RemoveFeedFile','$cookies','$upload','$timeout','$routeParams','LoadFeed','Comments','$rootScope','ngNotify',function($scope,CourseDetails,FeedFileDownload, RemoveFeedPost , RemoveFeedFile,$cookies,$upload, $timeout, $routeParams,LoadFeed, Comments,$rootScope, ngNotify) {

   $rootScope.whichView = "CourseDetailCtrl";
   this.params = $routeParams;
   // var csrf = $cookies.csrftoken;
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
        //console.log($scope.toggled);
    }
    
    angular.element(document).on('click', function(e){ 
        if(e.target.className != "fourChoice"){
           $scope.toggled? $scope.changeToggle() : "";
        }
    });

    $scope.fileArray={
      Lecture : [],
      Tutorial: [],
      ExamPaper: [],
      Solution: []
    };

  var upload = function (myfiles,typeArray,content){
    $upload.upload({
      url: base_domain+'/lectut_api/upload/'+$routeParams.courseId+'/', 
      // upload.php script, node.js route, or servlet url
      file: myfiles,  
      // single file or an array of files (array is for html6 only)
      method: 'POST',
      headers: {'Content-Type':'multipart/form-data'}, 
      // only for html5
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
            //console.log('progress: ' + progressPercentage + '% ' +
            //evt.config.file.name);
            if($scope.filesAdded){
            $(".postOverlay").html( progressPercentage + '% <div class="waitingFor">Upload in progress. Please wait...</div>');
            }
            else{
            $(".postOverlay").html('<div class="waitingFor">Posting ...</div>');
            }
        }).success(function (data, status, headers, config) {
            //console.log('file ' + config.file.name + 'uploaded. Response: ' +
            //JSON.stringify(data));
            //console.log("data");
            var result = JSON.stringify(data);
            //console.log($scope.posts);
            $scope.posts.unshift(data.complete_post);
            //console.log("data");
            //console.log(data);
            //console.log("-------------------------");
            //console.log($scope.posts);
            // null the top box 
            $scope.thing.content = "";
            $scope.fileArray={
               Lecture : [],
               Tutorial: [],
               ExamPaper: [],
               Solution: []
             };
          // Notifiaction Success
             ngNotify.set('Successfully posted.', {
                   position:'top',
                   type:'success',
                   duration: 3000
             });
          $(".postOverlay").hide();
        });
  }


  $scope.update = function(files,type){
     $scope.fileArray[type] = $scope.fileArray[type].concat(files);
     //console.log(files);
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

          //console.log("Things dajlksdjsa ld");
          //console.log(things);
          //console.log(!$scope.privacy);
          if(things.length == 0 && $scope.thing.content == ""){
            //alert("Post cannot be empty");
            ngNotify.set('Empty post is not allowed.', {
                   position:'top',
                   type:'error',
                   duration: 3000
             });
          }
          else{
            if(things.length !=0){
              $scope.filesAdded = true;
            }
            else{
              $scope.filesAdded = false;
            }
            $(".postOverlay").show();
            upload(things,typeData,$scope.thing.content);
          }
          //console.log("----------------");
          //console.log(typeData);
  }

  $scope.deleteItem = function(item, type){
        $scope.fileArray[type].splice(item,1);
        //console.log($scope.fileArray[type]);
  }

  // ------------------------- Comments -----------------------
  $scope.loadCommentsFunc = function(id){
    if($('#postComments_'+id).hasClass("open")){
        $('#postComments_'+id).removeClass("open");
        $('#postComments_'+id).html("");
    }
    else{
      $('#postComments_'+id).addClass("open");
      var promiseComments = Comments.getComments(id);
            promiseComments.then(function(x){
            //console.log("------Common fgeed commne-----------");
            //console.log(id);
            $('#postComments_'+id).append(x);
      });
    }
  }

  //-------------------------- Posts---------------------------
  // Loads the feed automatically on reload on a specific url.
  // check http://172.25.55.156:9008/course/3/feeds : feeds will be loaded.
  $scope.courseId = this.params.courseId;
  //$scope.courseName = "Physics and Chemistry";

  var promiseCourseData = CourseDetails.getCourseDetailsData($scope.courseId);
    promiseCourseData.then(function (d) {
       $scope.posts = d.posts;
       $scope.is_member = d.in_batch;
       //console.log("a");
    });

  $scope.getFeedData = function(id){
    //console.log("asdsad");
    var promiseCourseData = CourseDetails.getCourseDetailsData(id);

    promiseCourseData.then(function (d) {
       $scope.posts = d.posts;
       $scope.is_member = d.in_batch;
       //console.log("b");
    });
  }
  
  $scope.downloadFeedFile = function(id){
    //console.log("herecomesid");
    //console.log(id);
    var promiseFeedFileDownload = FeedFileDownload.getFeedFile(id);
    promiseFeedFileDownload.then(function(d){
          //console.log("gai aur ayi downl rq");
          var blob = new Blob([d], {type: "image/jpeg"});
              var objectUrl = URL.createObjectURL(blob);
                  window.open(objectUrl);
    });
  }

  $scope.removeFeedPost = function(id, index){
    //console.log("This is to be deleted.. "+id);
    //console.log($scope.posts);

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
              //console.log("Deleted this man"+ id);
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
    //console.log("This is to be deleted.. "+id);
    //console.log($scope.posts);

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
                 //console.log("Deleted this file man"+ id);
                 $scope.posts[parentIndex].files.splice(index,1);
                 //console.log($scope.posts[parentIndex]);
                 if($scope.posts[parentIndex].files.length == 0 && $scope.posts[parentIndex].post.content == ""){
                      $scope.posts.splice(parentIndex,1)
                 }
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


}]);

lectutApp.controller('CourseFeedsCtrl', ['$stateParams','$scope', function($stateParams,$scope) {

}]);

lectutApp.controller('CourseFilesCtrl', [ 'DataTables', 'DTOptionsBuilder' , 'DTColumnBuilder','DTInstances', '$scope', '$compile', '$routeParams','$rootScope',function( DataTables, DTOptionsBuilder, DTColumnBuilder, DTInstances,$scope, $compile, $routeParams, $rootScope) {
   //console.log("++++++++++++++++Course Files Ctrl+++++++++++++++");
   
   var promiseCourseData = DataTables.getTable($routeParams.courseId);
   $rootScope.whichView = "CourseFilesCtrl";
   $scope.selected = {};
   
   $scope.dtOptions = DTOptionsBuilder.fromFnPromise(
     promiseCourseData.then(
      function(d){
        //console.log(d);
        var allFiles = [];
        allFiles = allFiles.concat(d.archiveFiles.Tutorial);
        allFiles = allFiles.concat(d.archiveFiles.Lecture);
        allFiles = allFiles.concat(d.archiveFiles['Exam Papers']);
        allFiles = allFiles.concat(d.archiveFiles.Solution);
        allFiles = allFiles.concat(d.archiveFiles.Question);
        allFiles = allFiles.concat(d.currentFiles.Tutorial);
        allFiles = allFiles.concat(d.currentFiles.Lecture);
        allFiles = allFiles.concat(d.currentFiles['Exam Papers']);
        allFiles = allFiles.concat(d.currentFiles.Solution);
        allFiles = allFiles.concat(d.currentFiles.Question);
        return allFiles;
      }
   )
   ).withOption('createdRow', function(row, data, dataIndex) {
   // Recompiling so we can bind Angular directive to the DT
       $compile(angular.element(row).contents())($scope);
   }).withOption('paging',true).withOption('compact','true')
   .withPaginationType('full_numbers');
 
   $scope.dtColumns = [
             /*DTColumnBuilder.newColumn(null).withTitle('<div type="checkbox">Mark</div>').notSortable()
                 .renderWith(function(data, type, full, meta) {
                 return '<input type="checkbox" ng-change="toggleOne('+ data.id+')" ng-checked="selected['+data.id+']" ng-model="$scope.selected[' + data.id + ']">';
             }),*/
             // DTColumnBuilder.newColumn('id').withTitle('ID'),
             DTColumnBuilder.newColumn(null).withTitle('<span>File Name</span>')
             .renderWith(function(data,type,full){
                 //console.log(full.file_type);
                 var html= "";
                 //html += '<input type="checkbox" style="margin-right:10px;margin-left:5px;" ng-change="toggleOne('+ data.id+')" ng-checked="selected['+data.id+']" ng-model="$scope.selected[' + data.id + ']">';
                /* <i ng-show='file.file_type == "ppt"' class="fa fa-file-powerpoint-o"></i>
                 <i ng-show='file.file_type == "zip"' class="fa fa-file-archive-o"></i>
                 <i ng-show='file.file_type == "other"' class="fa fa-file"></i>
                  */
                 if(full.file_type == "image"){
                   html += '<img style="margin-right:10px; width:20px;height:20px; vertical-align: middle;" ng-src="{[base_domain]}/'+full.filepath+'"></img><span> <a download ng-href="{[base_domain]}/lectut_api/download/'+ full.id+'">'+full.upload_file+'</a></span>';
                 } 
                 else if(full.file_type == "ppt"){
                   html += '<i class="fa fa-file-powerpoint-o" style="margin-right:15px; font-size:21px;"></i><span><a download ng-href="{[base_domain]}/lectut_api/download/'+full.id+'">'+full.upload_file+'</a></span>';
                 }
                 else if(full.file_type == "zip"){
                   html += '<i class="fa fa-file-archive-o" style="margin-right:15px; font-size:21px;"></i><span><a download ng-href="{[base_domain]}/lectut_api/download/'+full.id+'">'+full.upload_file+'</a></span>';
                 }

                 else if(full.file_type == "pdf"){
                   html += '<i class="fa fa-file-pdf-o" style="margin-right:15px; font-size:21px;"></i><span><a download ng-href="{[base_domain]}/lectut_api/download/'+full.id+'">'+full.upload_file+'</a></span>';
                 }
                  else if(full.file_type == "sheet"){
                   html += '<i class="fa fa-file-excel-o" style="margin-right:15px; font-size:21px;"></i><span><a download ng-href="{[base_domain]}/lectut_api/download/'+full.id+'">'+full.upload_file+'</a></span>';
                 }
                else if(full.file_type == "doc"){
                   html += '<i class="fa fa-file-word-o" style="margin-right:15px; font-size:21px;"></i><span><a download ng-href="{[base_domain]}/lectut_api/download/'+full.id+'">'+full.upload_file+'</a></span>';
                 }
                 else{
                   html += '<i class="fa fa-file-o" style="margin-right:15px; font-size:21px;"></i><span><a download ng-href="{[base_domain]}/lectut_api/download/'+full.id+'">'+full.upload_file+'</a></span>';
                 }
                html += '<span class="fileShowUser">by: '+full.username+'</span>';
                html += '<span class="fileShowDownloads">Downloads: '+full.download_count+'</span>';
                html += '<div style="display: inline-block; float:right;margin-left:10px;"><a style="text-decoration:none" ng-href="#/course/{[courseId.courseId]}/files/'+full.id+'""><i class="fa fa-external-link fileSetting"></i></a></div>';
                return html;
             }),
            // DTColumnBuilder.newColumn('description').withTitle('Name'),
             DTColumnBuilder.newColumn('upload_type').withTitle('Type').notSortable().notVisible(),
             DTColumnBuilder.newColumn('datetime_created').withTitle('Share Date')
             .renderWith(function(data, type, full, meta) {
                 //console.log(data);
                 var html = "";
                 html += '<div style=" display: inline-block;"><span class="timeFile">'+ moment(data).format("DD-MM-YY, HH:mm");+'</span></div>'; 
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
          /*
         var table = $(".dataTable").DataTable();
         console.log(table);
         //table.column(0).visible('false'); 
         table.columns().indexes().flatten().each( function ( i ) {
             if(i==1){
             var column = table.column( i );
             var select = $('<select id="fileFilterType"><option value=""></option></select>')
             .appendTo( $(".dataTables_wrapper") )
             .on( 'change', function () {
              /*var val = $.fn.dataTable.util.escapeRegex(
                  $(this).val()
              );
              var val;
              var temp = $(this).val();
              if(temp == "Lecture"){
                val = "lec";
              }
              else if("Tutorial"){
                val = "tut"
              }
              else if("Exam Paper"){
                val = "exp"
              }
              else if("Solution"){
                val = "sol"
              }
               column.search( val ? '^'+val+'$' : '', true, false ).draw();
               } );

               column.data().unique().sort().each( function ( d, j ) {
                 select.append( '<option value="'+d+'">'+d+'</option>' )
               });
         } });*/
     });

       // Table Upload Type implementation
       function loadFileType(){
       if($(".dataTable").length != 0){
         var table = $(".dataTable").DataTable();
         //console.log("_+_+_+_+_+_+");
         //if(table){
         //  console.log("_________________________________");
         //}
         //console.log(table);
         //table.column(0).visible('false'); 
         table.columns().indexes().flatten().each( function ( i ) {
             if(i==1){
             var column = table.column( i );
             var select = $('<select id="fileFilterType"><option value="">All Files</option></select><div id="fileFilterArrow">&#x25BC;</div>')
             .appendTo( $(".dataTables_wrapper") )
             .on( 'change', function () {
               var val = $.fn.dataTable.util.escapeRegex(
                 $(this).val()
                );
            
               column
               .search( val ? '^'+val+'$' : '', true, false )
               .draw();
               } );

              //column.data().unique().sort().each( function ( d, j ) {
               select = $("#fileFilterType");
               select.append( '<option value="Lecture">Lectures</option>' );
               select.append( '<option value="Tutorial">Tutorials</option>' );
               select.append( '<option value="Exam Paper">Exam Papers</option>' );
               select.append( '<option value="Solution">Solutions</option>' );
               //select.append( '<option value="que">'+Question+'</option>' );
              // } );
         } });
       }
       else{
         setTimeout(function(){ loadFileType(); }, 500);
       }
       }

       loadFileType();
      // ------------------------------
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
      //console.log(d);
    });
}]);


lectutApp.controller('CourseOnePostCtrl', ['LoadOnePost','$scope','$routeParams','FeedFileDownload','RemoveFeedPost' ,'RemoveFeedFile','Comments', '$rootScope','$location','ngNotify',function(LoadOnePost, $scope, $routeParams, FeedFileDownload, RemoveFeedPost, RemoveFeedFile, Comments, $rootScope, $location,ngNotify) {
    //console.log($routeParams);
    $rootScope.whichView = "CourseOnePostCtrl";
    var promiseMembers = LoadOnePost.getOnePost($routeParams.courseId,$routeParams.postId);
    promiseMembers.then(function(d){
      $scope.onePost = d.post;
      $scope.is_member = d.in_batch;
      //console.log(d);
    });

  // ------------------------- Comments -----------------------
  $scope.loadCommentsFunc = function(id){
    if($('#postComments_'+id).hasClass("open")){
        $('#postComments_'+id).removeClass("open");
        $('#postComments_'+id).html("");
    }
    else{
      $('#postComments_'+id).addClass("open");
      var promiseComments = Comments.getComments(id);
            promiseComments.then(function(x){
            //console.log("------One Post Comments-----------");
            //console.log(id);
            $('#postComments_'+id).append(x);
      });
    }
  }
  $scope.removeFeedPost = function(id, index){
    //console.log("This is to be deleted.. "+id);
    //console.log($scope.onePost);

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
              //console.log("Deleted this man"+ id);
              //console.log($scope.onePost);
              $scope.onePost={};
              sweetAlert("Deleted!", "Post has been deleted.", "success");

               // redirect on file delete to main course page. 
                 var back_to_course = $location.path();
                 var i=0;
                 for(i=back_to_course.length; i>=0;i--){
                  if(back_to_course[i] == '/'){
                    break;
                  }
                 }
                 back_to_course = back_to_course.slice(0,i);
                 //console.log(base_domain+"/#"+back_to_course);
                 window.location = "/lectut/#"+back_to_course;

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
    //console.log("This is to be deleted.. "+id);
    // one 
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
                 //console.log("Deleted this file man"+ id);
                 $scope.onePost.files.splice(index,1);
                 sweetAlert("Deleted!", "File has been deleted.", "success");
                 //console.log(d);
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

lectutApp.controller('CourseOneFileCtrl', ['LoadOneFile','$scope','$routeParams','FeedFileDownload','RemoveFeedFile','$rootScope','$location','ngNotify',function(LoadOneFile, $scope, $routeParams, FeedFileDownload, RemoveFeedFile, $rootScope, $location, ngNotify) {
    //console.log($routeParams);
    $rootScope.whichView = "CourseOneFileCtrl";
    var promiseMembers = LoadOneFile.getOneFile($routeParams.courseId,$routeParams.fileId);
    promiseMembers.then(function(d){
      $scope.oneFile = d;
      //console.log("----------Thsi is one File.");
      //console.log(d);
    });

   $scope.removeFeedFile = function(id, parentIndex, index){
    //console.log("This is to be deleted.. "+id);
    // one file
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
                 //console.log("Deleted this file man"+ id);
                 $scope.oneFile=[];
                 sweetAlert("Deleted!", "File has been deleted.", "success");
                 //console.log(d);
                 // redirect on file delete to main course page. 
                 var back_to_course = $location.path();
                 var i=0;
                 for(i=back_to_course.length; i>=0;i--){
                  if(back_to_course[i] == '/'){
                    break;
                  }
                 }
                 back_to_course = back_to_course.slice(0,i);
                 //console.log(base_domain+"/#"+back_to_course);
                 window.location = "/lectut/#"+back_to_course;
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


lectutApp.controller('FacultyCtrl', ['$scope','$routeParams','$rootScope','$location','ngNotify','LoadFacultyData','DataTables', 'DTOptionsBuilder' , 'DTColumnBuilder','DTInstances','$compile',function($scope, $routeParams, $rootScope, $location, ngNotify, LoadFacultyData,DataTables, DTOptionsBuilder, DTColumnBuilder, DTInstances,$compile) {
    $rootScope.whichView = "FacultyCtrl";
    var promiseFacultyData = LoadFacultyData.getFacultyData($routeParams.facultyId);
   
   var courseNamekeys = [];

   
   $scope.dtOptions = DTOptionsBuilder.fromFnPromise(
     promiseFacultyData.then(
      function(d){
        //console.log(d);
        $scope.facultyData = d;
        var allFiles = [];
        for (var key in d.Files) {
           if (d.Files.hasOwnProperty(key)) {
               // Modelling & Simulation£$£$2323
               var keyArray = key.split(";;;;");
               var key_courseName = keyArray[0];
               var key_courseId = keyArray[1];
               var obj = d.Files[key];
               courseNamekeys.push(key_courseName);
               for(var i=0;i<obj.length;i++){
                  obj[i].course_name = key_courseName;
                  obj[i].course_id = key_courseId;
               }
               allFiles = allFiles.concat(obj);
            }
        }
        return allFiles;
      }
   )
   ).withOption('createdRow', function(row, data, dataIndex) {
   // Recompiling so we can bind Angular directive to the DT
       $compile(angular.element(row).contents())($scope);
   }).withOption('paging',true).withOption('compact','true')
   .withPaginationType('full_numbers');
 
   $scope.dtColumns = [
             DTColumnBuilder.newColumn(null).withTitle('<span>File Name</span>')
             .renderWith(function(data,type,full){
                 var html= "";
                 if(full.file_type == "image"){
                   html += '<img style="margin-right:10px; width:20px;height:20px; vertical-align: middle;" ng-src="{[base_domain]}/'+full.filepath+'"></img><span> <a download ng-href="{[base_domain]}/lectut_api/download/'+ full.id+'">'+full.upload_file+'</a></span>';
                 } 
                 else if(full.file_type == "ppt"){
                   html += '<i class="fa fa-file-powerpoint-o" style="margin-right:15px; font-size:21px;"></i><span><a download ng-href="{[base_domain]}/lectut_api/download/'+full.id+'">'+full.upload_file+'</a></span>';
                 }
                 else if(full.file_type == "zip"){
                   html += '<i class="fa fa-file-archive-o" style="margin-right:15px; font-size:21px;"></i><span><a download ng-href="{[base_domain]}/lectut_api/download/'+full.id+'">'+full.upload_file+'</a></span>';
                 }

                 else if(full.file_type == "pdf"){
                   html += '<i class="fa fa-file-pdf-o" style="margin-right:15px; font-size:21px;"></i><span><a download ng-href="{[base_domain]}/lectut_api/download/'+full.id+'">'+full.upload_file+'</a></span>';
                 }
                  else if(full.file_type == "sheet"){
                   html += '<i class="fa fa-file-excel-o" style="margin-right:15px; font-size:21px;"></i><span><a download ng-href="{[base_domain]}/lectut_api/download/'+full.id+'">'+full.upload_file+'</a></span>';
                 }
                else if(full.file_type == "doc"){
                   html += '<i class="fa fa-file-word-o" style="margin-right:15px; font-size:21px;"></i><span><a download ng-href="{[base_domain]}/lectut_api/download/'+full.id+'">'+full.upload_file+'</a></span>';
                 }
                 else{
                   html += '<i class="fa fa-file-o" style="margin-right:15px; font-size:21px;"></i><span><a download ng-href="{[base_domain]}/lectut_api/download/'+full.id+'">'+full.upload_file+'</a></span>';
                 }
                html += '<span class="fileShowDownloads">Downloads: '+full.download_count+'</span>';
                html += '<div style="display: inline-block; float:right;margin-left:10px;"><a style="text-decoration:none" ng-href="#/course/'+ full.course_id+'/files/'+full.id+'""><i class="fa fa-external-link fileSetting"></i></a></div>';
                return html;
             }),
            // DTColumnBuilder.newColumn('description').withTitle('Name'),
             DTColumnBuilder.newColumn('upload_type').withTitle('Type').notSortable().notVisible(),
             DTColumnBuilder.newColumn('course_name').withTitle('Course Name').renderWith(function(data,type,full){
              var html="";
              html+='<span class="course_name_in_datatable">'+data+'</span>';
              return html;
             }).notSortable(),
             DTColumnBuilder.newColumn('datetime_created').withTitle('Share Date')
             .renderWith(function(data, type, full, meta) {
                 //console.log(data);
                 var html = "";
                 html += '<div style=" display: inline-block;"><span class="timeFile">'+ moment(data).format("DD-MM-YY, HH:mm");+'</span></div>'; 
                 return html;
             })/*
             DTColumnBuilder.newColumn(null).withTitle('').notSortable()
             .renderWith(function(data, type, full, meta) {
                 //return '<div class="downloadFile" ng-click="toggleAll()">Download</div>';
                 return '<i class="fa fa-cog fileSetting" ng-click="toggleAll()"></i>';
             })*/
      ];
      
      // DTInstances.getLast().then(function (dtInstance) {
      //     dtInstance.DataTable.data().each(function(data) {
      //          $scope.selected[data.id] = false;
      //     });
      
      // });

       // Table Upload Type implementation
       function loadFileType(){
       if($(".dataTable").length != 0){
         var table = $(".dataTable").DataTable();
         table.columns().indexes().flatten().each( function ( i ) {
             if(i==1){
             var column = table.column( i );
             var select = $('<select id="fileFilterType"><option value="">All types</option></select><div id="fileFilterArrow">&#x25BC;</div>')
             .appendTo( $(".dataTables_wrapper") )
             .on( 'change', function () {
               var val = $.fn.dataTable.util.escapeRegex(
                 $(this).val()
                );
            
               column
               .search( val ? '^'+val+'$' : '', true, false )
               .draw();
               } );

              //column.data().unique().sort().each( function ( d, j ) {
               select = $("#fileFilterType");
               select.append( '<option value="Lecture">Lectures</option>' );
               select.append( '<option value="Tutorial">Tutorials</option>' );
               select.append( '<option value="Exam Paper">Exam Papers</option>' );
               select.append( '<option value="Solution">Solutions</option>' );
               //select.append( '<option value="que">'+Question+'</option>' );
              // } );
         } });
       }
       else{
         setTimeout(function(){ loadFileType(); }, 500);
       }
       }

       loadFileType();

       // Table Upload Type implementation
       function courseSelect(){
       if($(".dataTable").length != 0){
         var table = $(".dataTable").DataTable();
         table.columns().indexes().flatten().each( function ( i ) {
             if(i==2){
             var column = table.column( i );
             var select = $('<select id="courseFilterType"><option value="">All Courses</option></select><div id="courseFilterArrow">&#x25BC;</div>')
             .appendTo( $(".dataTables_wrapper") )
             .on( 'change', function () {
               var val = $.fn.dataTable.util.escapeRegex(
                 $(this).val()
                );
            
               column
               .search( val ? '^'+val+'$' : '', true, false )
               .draw();
               } );

              select = $("#courseFilterType");
              for(var i=0; i<courseNamekeys.length;i++){
                select.append( '<option value="'+courseNamekeys[i]+'">'+courseNamekeys[i]+'</option>' );
              }
         } });
       }
       else{
         setTimeout(function(){ courseSelect(); }, 500);
       }
       }

       courseSelect();


}]);


lectutApp.controller('FourNotCtrl', ['$scope','$routeParams','$rootScope','$location','ngNotify',function($scope, $routeParams,$rootScope, $location, ngNotify) {
    //console.log($routeParams);
    $rootScope.whichView = "FourNotCtrl";


}]);