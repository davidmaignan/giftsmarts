(function() {
    "use strict";

    function routes($routeProvider, $locationProvider) {
        $routeProvider
            .when('/', {
                templateUrl: '/static/partials/index.html',
                controller: 'IndexCtrl'
            })
            .when('/login/', {
                templateUrl: '/static/partials/login.html'
            })
            .when('/dashboard/', {
                templateUrl: '/static/partials/dashboard.html',
                controller: 'DashboardCtrl'
            })
            .otherwise({
                redirectTo: '/404/'
            });

        $locationProvider.html5Mode(true);
    }


    angular.module('app').config(routes);
})();
