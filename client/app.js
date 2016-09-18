var app = angular.module('GreatAppAgain',['ngMaterial', 'ngMessages', 'material.svgAssetsCache', 'ngRoute', "chart.js"])

.config(function($mdThemingProvider, $routeProvider, $locationProvider) {
  $mdThemingProvider.theme('dark-grey').backgroundPalette('grey').dark();
  $mdThemingProvider.theme('dark-orange').backgroundPalette('orange').dark();
  $mdThemingProvider.theme('dark-purple').backgroundPalette('deep-purple').dark();
  $mdThemingProvider.theme('dark-blue').backgroundPalette('blue').dark();

  $routeProvider

		// route for the home page
		.when('/', {
			templateUrl : 'pages/home.html',
			controller: 'GreatCtrl'
		})

		.when('/about', {
			templateUrl: 'pages/about.html'
		})

		.when('/insight', {
			templateUrl: 'pages/insight.html',
			controller: 'GreatCtrl'
		})

		.otherwise({templateUrl: 'pages/404.html'})

		// use the HTML5 History API to get the pretty urls without a weird /#/ between relevant info
        $locationProvider.html5Mode(true);
});
