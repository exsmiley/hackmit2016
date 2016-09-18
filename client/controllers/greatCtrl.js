app.controller('GreatCtrl', function($scope, $http) {
	// use for loading????
  	$scope.imagePath = 'img/washedout.png';
  	$scope.trumpVotes = 0
  	$scope.hillaryVotes = 0

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
		    $scope.nextImage()
		  })
	  })

	// set the display image
	$scope.nextImage = function() {
		var cand = Math.floor(Math.random()*2)
		if(cand === 0) {
			$scope.cand = 'trump'
			var index = Math.floor(Math.random()*$scope.trumpImages.length+1)
			$scope.currentImage = $scope.trumpImages[index]
			$scope.trumpImages.splice(index, 1)
		}
		else {
			$scope.cand = 'hillary'
			var index = Math.floor(Math.random()*$scope.hillaryImages.length+1)
			$scope.currentImage = $scope.hillaryImages[index]
			$scope.hillaryImages.splice(index, 1)
		}
		$scope.$apply()
	}

  	// vote for the current candidate
  	$scope.vote = function() {
  		if($scope.cand === 'trump') {
  			$scope.trumpVotes++
  		}
  		else {
  			$scope.hillaryVotes++
  		}
  		$scope.nextImage()
  	}
})