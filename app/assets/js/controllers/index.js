(function(){
    "use strict";
    function IndexCtrl($scope, FriendRelationshipService) {

        FriendRelationshipService.find_all({},
            function(res){
                console.log(res);
//                $scope.username = res.username;

            }, function(err){
                console.error(err);
            });

        $scope.phones = [
            {'name': 'Nexus S',
             'snippet': 'Fast just got faster with Nexus S.'},
            {'name': 'Motorola XOOM™ with Wi-Fi',
             'snippet': 'The Next, Next Generation tablet.'},
            {'name': 'MOTOROLA XOOM™',
             'snippet': 'The Next, Next Generation tablet.'}
          ];
    }

    angular.module("app").controller('IndexCtrl', IndexCtrl);
})();