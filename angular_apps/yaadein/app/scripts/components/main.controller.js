'use strict';

var app = angular.module('yaadeinApp');
var originURL = base_domain;

app.controller('YaadeinController', ['$scope', '$http', '$q', '$timeout', '$upload', '$location', '$routeParams', '$route', 'ngNotify', 'TickerService', 'HomeService', 'PostService', 'Lightbox', 'SweetAlert',
    function ($scope, $http, $q, $timeout, $upload, $location, $routeParams, $route, ngNotify, TickerService, HomeService, PostService, Lightbox, SweetAlert) {

    ngNotify.config({
      theme: 'pure',
      position: 'top',
      duration: 2000,
      sticky: false
    });

	$scope.appname = 'Yaadein';

	$scope.navigationItems = [
		{
			'id': 'profile',
			'class': 'fa fa-user',
			'url': '#/profile/',
			'hint': 'Profile'
		},
    {
      'id': 'home',
      'class': 'fa fa-bars',
      'url': '#/',
      'hint': 'Feed'
    },
		{
			'id': 'search',
			'class': 'fa fa-search',
			'url': '#',
			'hint': 'Search'
		},
		{
			'id': 'post',
			'class': 'fa fa-pencil-square-o',
			'url': '#',
			'hint': 'Post'
		},
		//{
			//'id': 'notifications',
			//'class': 'fa fa-bell',
			//'url': '#',
			//'hint': 'Notifications'
		//},
		{
			'id': 'signOut',
			'class': 'fa fa-sign-out',
			'url': originURL+'/logout/',
			'hint': 'Sign Out'
		}
	];

	$scope.currentNavItem = $scope.navigationItems[1];
  $scope.lastNavItem = $scope.navigationItems[1];

	$scope.setCurrentNavItem = function (navItem) {
    if(navItem === null) {
      $scope.currentNavItem = {};
      return;
    }
    $scope.lastNavItem = $scope.currentNavItem;
		$scope.currentNavItem = navItem;
		if ($scope.currentNavItem.id === 'search' || $scope.currentNavItem.id === 'post') {
			$('#centered').addClass('blur-back');
			$('.right-sidebar').addClass('blur-back');
		} else {
      $location.path(navItem.url);
			$('#centered').removeClass('blur-back');
			$('.right-sidebar').removeClass('blur-back');
		}
	};

	$scope.isCurrentNavItem = function (navItem) {
		return $scope.currentNavItem !== null && $scope.currentNavItem.id === navItem.id;
	};

	$scope.getCurrentNavItem = function () {
		return $scope.currentNavItem.id;
	};

  $scope.enlargeImage = function (images, index, ev) {
    ev.preventDefault();
    Lightbox.openModal(images, index);
  }; 

	$scope.closePost = function () {
		$('#centered').removeClass('blur-back');
		$('.right-sidebar').removeClass('blur-back');
		$('#postBox').fadeOut(300);
		$scope.setCurrentNavItem($scope.navigationItems[1]);
    $scope.clearNewPostData();
	};

	$scope.closeSearch = function () {
    $('#centered').removeClass('blur-back');
		$('.right-sidebar').removeClass('blur-back');
		$('#searchBox').fadeOut(300);
    $scope.setCurrentNavItem($scope.navigationItems[1]);
	};

	$scope.showInviteBox = function () {
		$('#inviteBox').fadeIn(150);
    $('#centered').addClass('blur-back');
		$('.right-sidebar').addClass('blur-back');
    $scope.newPost.user_tags = [];
	};

	$scope.closeInvite = function () {
    $('#centered').removeClass('blur-back');
		$('.right-sidebar').removeClass('blur-back');
		$('#inviteBox').fadeOut(300);
    $scope.newPost.user_tags = [];
	};

  $scope.inviteUsers = function () {
    var prom = TickerService.inviteUsers($scope.newPost.user_tags);
    prom.then(function (x) {
        if (x === 'True') {
          ngNotify.set('Invites have been sent!', 'success');
          $scope.closeInvite();
        } else {
          ngNotify.set('Could not send invites.', 'error');
        }
    });
  };

  $scope.showCoverHint = function () {
    $('#cover-upload-hint').fadeIn(150);
  };

  $scope.hideCoverHint = function () {
    $('#cover-upload-hint').fadeOut(150);
  };

  $scope.addOriginToImageUrl = function (resp) {
    var results = resp.results;
    for(var i = 0; i < results.length; i += 1) {
      results[i].profile_pic = originURL + results[i].profile_pic;
      results.id;
    }
    return resp;
  };

  $scope.personSelected = function(selected) {
    $scope.setCurrentNavItem({});
    $location.path('/profile/' + selected.originalObject.id);
  };

	$scope.user = {};
  var LoggedUserData = HomeService.getLoggedUser();
  LoggedUserData.then(function (d) {
      $scope.user = d;
      $scope.navigationItems[0].url += $scope.user.enrolmentNo;
      $scope.navigationItems[0].hint = $scope.user.name;
  });

	//Append enrolment number to profile and gallery URLs
	//$scope.navigationItems[0].url += $scope.user.enrolmentNo;

	$scope.trending = [];
	var tickPromise = TickerService.getTrending();
	tickPromise.then(function (d) {
		$scope.trending = d.hashed;
	});

  $scope.newPost = {
    'post_owner': $scope.user.name,
    'post_owner_enrol': $scope.user.enrolmentNo,
    'post_owner_branch': $scope.user.label,
    'post_owner_pic': $scope.user.profilePic,
    'time': '',
    'image_url': [],
    'post_text': '',
    'user_tags': [],
    'spot': [],
    'post_type': 'A'
  };

  //$scope.postStatus = false;

  //$scope.$watch(function (scope) {
  //      return scope.postStatus;
  //    }, function (newValue, oldValue, scope) {
  //    if(scope.postStatus) {
  //      scope.newPost.post_type = 'B';
  //      console.log(scope.newPost.post_type);
  //    } else {
  //      scope.newPost.post_type = 'A';
  //      console.log(scope.newPost.post_type);
  //    }
  //});

  $scope.clearNewPostData = function () {
    $scope.newPost.post_text = '';
    $scope.newPost.user_tags = [];
    $scope.newPost.image_url = [];
    $scope.images1.imageArray = [];
  };

  $scope.loadTags = function (query) {
    var defer = $q.defer();
    $http.get(originURL + '/yaadein_api/search/4/?q=' + query, {ignoreLoadingBar: true})
      .success(function (d) {
          defer.resolve(d.results);
    });
    return defer.promise;
  };

  $scope.loadSpots = function (query) {
    var defer = $q.defer();
    $http.get(originURL + '/yaadein_api/search/2/?q=' + query, {ignoreLoadingBar: true})
      .success(function (d) {
          defer.resolve(d.results);
    });
    return defer.promise;
  };

  $scope.$watch('coverpic', function (photo) {
      if (photo !== null) {
        (function(file){
         $scope.uploadCover(file);
        })(photo);
      }
  });

  $scope.images1 = {
      'imageArray': []
  };

  $scope.addImage = function (files) {
    $scope.images1.imageArray = $scope.images1.imageArray.concat(files);
  };

  $scope.deleteImage = function (i) {
    $scope.images1.imageArray.splice(i, 1);
  };

  $scope.deleteAllImages = function () {
    $scope.images1.imageArray = [];
  };

  $scope.upload = function (files) {
    var uploadUrl = originURL + '/yaadein_api/user/' + $scope.user.enrolmentNo + '/';
    if ($routeParams && $routeParams.enrolmentNo) {
      uploadUrl = originURL + '/yaadein_api/user/' + $routeParams.enrolmentNo + '/';
    }
    var sizeExceeded = false;
    for(var j = 0; j < files.length; j += 1) {
      if (files[j].size > 2097152) {
        sizeExceeded = true;
      }
    }
    //for(var i = 0; i < files.length; i += 1) {
    //var file = files[i];
    if(files.length < 11 && $scope.newPost.post_text!=='' && !sizeExceeded) {
      $('#uploadButton').prop('disabled', true);
      $upload.upload({
        url: uploadUrl,
        headers: {'Content-Type':'multipart/form-data'}, 
        method: 'POST',
        data: {
          post_text: $scope.newPost.post_text,
          user_tags: $scope.newPost.user_tags,
          spot: $scope.newPost.spot,
          post_type: $scope.newPost.post_type
        },
        file: files,
        withCredentials: true
      }).progress(function (evt) {
        $('#loading').fadeIn(100);
      }).success(function (data, status, headers, config) {
        $('#loading').fadeOut(100);
        var postPromise = PostService.getPost(data.posts_data[0].post_id);
        postPromise.then(function (d) {
          d.post_owner_pic = originURL + d.post_owner_pic;
          for(var j = 0; j < d.image_url.length; j += 1) {
            d.image_url[j] = originURL + d.image_url[j];
          }
          $scope.user.posts_data.unshift(d);
        });
        $scope.closePost();
        ngNotify.set('Successfully posted!', 'success');
      }).error(function(data, status, headers, config) {
        $('#loading').fadeOut(100);
        ngNotify.set('Could not post!', 'error');
        $('#uploadButton').prop('disabled', false);
      });
    } else {
      if(files.length > 10) {
        ngNotify.set('Maximum 10 photos are allowed.', 'warn');
      } else if(sizeExceeded) {
        ngNotify.set('Maximum file size for a photo is 2MB', 'warn');
      } else if($scope.newPost.post_text === '')  {
        ngNotify.set('Type in some memories', 'warn');
        $('#postMessageInput').addClass('error');
        $('#postMessageInput').focus();
      }
    }
  };

  $scope.uploadCover = function (files) {
    if (files && files.length === 1) {
      $upload.upload({
        url: originURL + '/yaadein_api/cover/upload/',
        headers: {'Content-Type':'multipart/form-data'}, 
        method: 'POST',
        data: {
        },
        file: files,
        withCredentials: true
      }).progress(function (evt) {
      }).success(function (data, status, headers, config) {
        ngNotify.set('Cover photo updated successfully!', 'success');
        location.reload();
      }).error(function (data, status, headers, config) {
        ngNotify.set('Could not update cover photo.', 'error');
      });
    }
  };

  $scope.isLoggedUserPost = function (id) {
    return $scope.user.enrolmentNo === id;
  };

  $scope.deletePost = function (id, index) {
    SweetAlert.swal({
      title: "Are you sure?",
      text: "Your post will be deleted forever",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",confirmButtonText: "Yes, delete it!",
      cancelButtonText: "No, cancel!",
      closeOnConfirm: false,
      closeOnCancel: false }, 
      function(isConfirm){ 
        if (isConfirm) {
          var flag = PostService.deletePost(id);
          flag.then(function (d) {
            if (d === 'True') {
              $scope.user.posts_data.splice(index, 1);
              SweetAlert.swal("Deleted!", "Your post has been deleted.", "success");
            } else {
              SweetAlert.swal("Error!", "Your post could not be deleted.", "error");
            }
           });
        } else {
          SweetAlert.swal("Cancelled", "Your post wasn't deleted!", "error");
        }
    });
  };

  //Emoji Service
  $scope.predictEmoji = function(term) {
    var emojiList = [];
    return $http.get('scripts/emojis.json')
      .then(function (response) {
          angular.forEach(response.data, function(item) {
            if (item.name.toUpperCase().indexOf(term.toUpperCase()) >= 0) {
              emojiList.push(item);
            }
          });
      $scope.emojis = emojiList;
      return $q.when(emojiList);
   });
  };

  $scope.getEmojiTextRaw = function(item) {
    return ':' + item.name + ':';
  };

  $scope.macros = {
	'brb': 'be right back',
	'omw': 'on my way',
  'ty': 'Thank you',
  'hbd': 'Happy Birthday!',
  'g2g': 'gotta go'
  };
}]);

app.controller('HomeController', ['$scope', '$http', 'HomeService', 
    function ($scope, $http, HomeService) {

	$scope.addToFeed = function () {
		$http.get('http://beta.json-generator.com/api/json/get/CHdvIym')
			.success(function (ds) {
				for(var i = 0; i < ds.length; i += 1) {
					$scope.posts.push(ds[i]);
				}
		});
	};

}]);

app.controller('ProfileController', ['$routeParams', '$scope', '$http', 'UserService', 'PostService', 'ngNotify', 'SweetAlert',
	function ($routeParams, $scope, $http, UserService, PostService, ngNotify, SweetAlert) {

	$scope.currentUser = {};
	var userPromise = UserService.getUser($routeParams.enrolmentNo);
	userPromise.then(function (d) {
			$scope.currentUser = d;

      //Add originURL to image URLs
      $scope.currentUser.profilePic = originURL + $scope.currentUser.profilePic;
      $scope.currentUser.coverPic = originURL + $scope.currentUser.coverPic;

      var posts = $scope.currentUser.posts_data;
      for (var i = 0; i < posts.length; i += 1) {
        posts[i].post_owner_pic = originURL + posts[i].post_owner_pic;
        for (var j = 0; j < posts[i].image_url.length; j += 1) {
          posts[i].image_url[j] = originURL + posts[i].image_url[j];
        }
      }
	});

  $scope.deleteProfilePost = function (id, index) {
    SweetAlert.swal({
      title: "Are you sure?",
      text: "Your post will be deleted forever",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",confirmButtonText: "Yes, delete it!",
      cancelButtonText: "No, cancel!",
      closeOnConfirm: false,
      closeOnCancel: false }, 
      function(isConfirm){ 
        if (isConfirm) {
          var flag = PostService.deletePost(id);
          flag.then(function (d) {
            if (d === 'True') {
              $scope.currentUser.posts_data.splice(index, 1);
              SweetAlert.swal("Deleted!", "Your post has been deleted.", "success");
            } else {
              SweetAlert.swal("Error!", "Your post could not be deleted.", "error");
            }
           });
        } else {
          SweetAlert.swal("Cancelled", "Your post wasn't deleted!", "error");
        }
    });
  };

  $scope.isLoggedUserProfile = function () {
    return $scope.user.enrolmentNo === $scope.currentUser.enrolmentNo;
  };

	$scope.addToFeed = function () {
		$http.get('http://beta.json-generator.com/api/json/get/CHdvIym')
			.success(function (ds) {
				for(var i = 0; i < ds.length; i += 1) {
					$scope.posts.push(ds[i]);
				}
		});
	};

}]);

app.controller('GalleryController', ['$routeParams', '$scope', 'dataUserService',
	function ($routeParams, $scope, UserService) {

	$scope.currentUser = {};
	var userData = UserService.getUser($routeParams.enrolmentNo);
	userData.then(function (d) {
    $scope.currentUser = d;
	});

}]);

app.controller('HashtagController', ['$routeParams', '$scope', '$http', 'HashtagService', 'PostService', 'ngNotify', 'SweetAlert',
	function ($routeParams, $scope, $http, HashtagService, PostService, ngNotify, SweetAlert) {

  $scope.hash = $routeParams.hashtag;  
	$scope.posts = [];
	var dataPromise = HashtagService.getHashtaggedPosts($routeParams.hashtag);
	dataPromise.then(function (d) {

    //Add originURL to image URLs
    for(var i = 0; i < d.posts_data.length; i += 1) {
      d.posts_data[i].post_owner_pic = originURL + d.posts_data[i].post_owner_pic;
      for(var j = 0; j < d.posts_data[i].image_url.length; j += 1) {
        d.posts_data[i].image_url[j] = originURL + d.posts_data[i].image_url[j];
      }
    }
    $scope.posts = d.posts_data;
  });

  $scope.deleteHashtagPost = function (id, index) {
    SweetAlert.swal({
      title: "Are you sure?",
      text: "Your post will be deleted forever",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",confirmButtonText: "Yes, delete it!",
      cancelButtonText: "No, cancel!",
      closeOnConfirm: false,
      closeOnCancel: false }, 
      function(isConfirm){ 
        if (isConfirm) {
          var flag = PostService.deletePost(id);
          flag.then(function (d) {
            if (d === 'True') {
              $scope.posts.splice(index, 1);
              SweetAlert.swal("Deleted!", "Your post has been deleted.", "success");
            } else {
              SweetAlert.swal("Error!", "Your post could not be deleted.", "error");
            }
           });
        } else {
          SweetAlert.swal("Cancelled", "Your post wasn't deleted!", "error");
        }
    });
  };
}]);

app.controller('PostController', ['$routeParams', '$scope', '$q', '$http', 'PostService',  
   function ($routeParams, $scope, $q, $http, PostService) {

   $scope.post = {};
   var postData = PostService.getPost($routeParams.postId);
   postData.then(function (d) {

     //Add originURL to image URLs
     for(var j = 0; j < d.image_url.length; j += 1) {
      d.image_url[j] = originURL + d.image_url[j];
     }

     d.post_owner_pic = originURL + d.post_owner_pic;
     $scope.post = d;
   });

}]);
