(function() {
    "use strict";

    function routes($routeProvider, $locationProvider) {
        $routeProvider
            .when('/', {
                templateUrl: '/static/partials/index.html',
                controller: 'IndexCtrl'
            })
            .when('/friend/:id', {
                templateUrl: '/static/partials/friend.html',
                controller: 'FriendCrtl'
            })
            .when('/login/', {
                templateUrl: '/static/partials/login.html'
            })
            .when('/dashboard/', {
                templateUrl: '/static/partials/dashboard.html',
                controller: 'DashboardCtrl'
            })
            .when('/contact_us/', {
                templateUrl: '/app/views/contact_us.html',
                controller: 'ContactUsCtrl'
            })
            .otherwise({
                redirectTo: '/404/'
            });

        $locationProvider.html5Mode(true);
    }


    angular.module('app').config(routes);
})();
