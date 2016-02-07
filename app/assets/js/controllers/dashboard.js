(function(){
    "use strict";
    function DashboardCtrl($scope, UserResource) {
        UserResource.get_username({},
            function(res){
                console.log(res.username);
                $scope.username = res.username;

            }, function(err){
                console.error(err);
                
            });
    }

    angular.module("app").controller('DashboardCtrl', DashboardCtrl);
})();