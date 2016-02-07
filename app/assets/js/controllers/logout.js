(function() {
    function LogoutCtrl($rootScope, $scope, $element, AuthenticationResource, $location) {

        $scope.logout = function() {
            // AuthenticationResource.logout()
            delete $rootScope.$storage.token;
            $location.path('/login/');

        };

    }

    angular.module("app").controller("LogoutCtrl", LogoutCtrl);
})();
