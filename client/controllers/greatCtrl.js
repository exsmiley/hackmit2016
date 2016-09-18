app.controller('GreatCtrl', function($scope, $http) {
	// use for loading????
  	$scope.imagePath = 'img/washedout.png';

  	// Get lists of images
  	$http({
	  method: 'GET',
	  url: '/api/images/trump',
	}).then(function successCallback(response) {
	    $scope.trumpImages = response['data']
	    $http({
		  method: 'GET',
		  url: '/api/images/hillary',
		}).then(function successCallback(response) {
		    $scope.hillaryImages = response['data']
		    $scope.setImage()
		  })
	  })

	// set the display image
	$scope.setImage = function() {
		var cand = Math.floor(Math.random()*2)
		if(cand === 0) {
			$scope.cand = 'trump'
			var index = Math.floor(Math.random()*$scope.trumpImages.length+1)
			$scope.currentImage = $scope.trumpImages[index]
			$scope.trumpImages.splice(index)
		}
		else {
			$scope.cand = 'hillary'
			var index = Math.floor(Math.random()*$scope.hillaryImages.length+1)
			$scope.currentImage = $scope.hillaryImages[index]
			$scope.hillaryImages.splice(index)
		}
	}

  	// vote for the current candidate
  	$scope.vote = function() {
  		// TODO
  	}

  	// moves on to the next picture in the reel
  	$scope.next = function() {
  		// TODO
  	}
})