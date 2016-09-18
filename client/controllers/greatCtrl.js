app.controller('GreatCtrl', function($scope, $http) {
	// use for loading????
  	$scope.imagePath = 'img/washedout.png';
  	$scope.trumpVotes = 0
  	$scope.hillaryVotes = 0
  	$scope.finished = false
  	$scope.pageIndex = 1

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
		  })
	  })

	// set the display image
	$scope.nextImage = function() {
		if($scope.trumpImages.length === 0 && $scope.hillaryImages.length === 0) {
			// no more images to cycle through
			$scope.finish()
			return
		}
		var cand = Math.floor(Math.random()*2)
		if(cand === 0) {
			$scope.cand = 'trump'
			if($scope.trumpImages.length === 0) {
				$scope.nextImage()
				return
			}
			var index = Math.floor(Math.random()*$scope.trumpImages.length)
			$scope.currentImage = $scope.trumpImages[index]
			$scope.trumpImages.splice(index, 1)
		}
		else {
			$scope.cand = 'hillary'
			if($scope.hillaryImages.length === 0) {
				$scope.nextImage()
				return
			}
			var index = Math.floor(Math.random()*$scope.hillaryImages.length)
			$scope.currentImage = $scope.hillaryImages[index]
			$scope.hillaryImages.splice(index, 1)
		}
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

  	// leaves the start page (or tied page) and starts the game
  	$scope.start = function() {
  		$scope.pageIndex = 2
  		$scope.nextImage()
  	}

  	// transitions to the final screen
  	$scope.finish = function() {
  		if($scope.trumpVotes === $scope.hillaryVotes) {
  			$scope.pageIndex = 4
  			return
  		}
  		else if($scope.trumpVotes > $scope.hillaryVotes) {
  			$scope.winner = 'Trump'
  		}
  		else {
  			$scope.winner = "Hillary"
  		}
  		$scope.pageIndex = 3

  		// POST the winner to the server
  		// $http.post('/api/vote', {"candidate": a});
  		$http({
		    method: 'POST',
		    url: '/api/vote',
		    data: "candidate=" + $scope.winner,
		    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
		});
  	}
})