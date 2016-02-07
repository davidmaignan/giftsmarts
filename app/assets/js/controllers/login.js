(function() {
    function LoginCtrl($rootScope, $scope, $element, AuthenticationResource, $location) {


        if($rootScope.$storage.token) {
            $location.path('/dashboard/');
        }

        $scope.login = {};

        $scope.sent = false;

        var vm = this;

        vm.response = null;

        $scope.clear = function() {
            $scope.login = {
                "username": "",
                "password": ""
            };
        };

        $scope.submit = function(form) {

            if (form.$invalid) {
                return;
            }

            $scope.sent = true;

            AuthenticationResource.login({
                "username": $scope.login.username,
                "password": $scope.login.password
            }, function(res){
                $scope.sent = true;
                $scope.success = true;

                $rootScope.$storage.token = res.token;

                $location.path('/dashboard/');

            }, function(err){
                console.error(err);
                $scope.sent = false;
            });
        };

        $scope.clear();
    }

    angular.module("app").controller("LoginCtrl", LoginCtrl);
})();
