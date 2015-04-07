'use strict';

var app = angular.module('yaadeinApp');

app.filter('romanNumber', function () {
  return function (input) {
    if (input === 1) {
    	return 'I';
    } else if (input === 2) {
    	return 'II';
    } else if (input === 3) {
    	return 'III';
    } else if (input === 4) {
    	return 'IV';
    } else {
    	return 'V';
    }
  };
});

app.filter('hashtags', ['$filter', function ($filter) {
	return function(text, target) {
		if (!text) {
			return text;
		}
		
		var replacedText = $filter('linky')(text, target);
		var targetAttr = '';
		if (angular.isDefined(target)) {
			targetAttr = ' target="' + target + '"';
		}
		// replace #hashtags and send them to twitter
		var replacePattern1 = /(|\s)#(\w*[a-zA-Z_]+\w*)/gim;
		replacedText = text.replace(replacePattern1, '$1<a href="#/hashtag/$2"' + targetAttr + ' class="hash">#$2</a>');
		// replace @mentions but keep them to our site
		//var replacePattern2 = /(^|\s)\@(\w*[a-zA-Z_]+\w*)/gim;
		//replacedText = replacedText.replace(replacePattern2, '$1<a href="https://twitter.com/$2"' + targetAttr + '>@$2</a>');
		return replacedText;
	};
}]);
