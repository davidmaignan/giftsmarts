(function(){
    "use strict";
    function FriendCrtl($scope, $routeParams, UserProductService, FriendRelationshipService) {
        console.log("FriendCrtl" + $routeParams.id);

        UserProductService.find_all({'userId': $routeParams.id},
            function(res){
                 $scope.user_products = res.data



                 console.log(res.data);
            }, function(err){
                console.log(err);
            }
        );

        FriendRelationshipService.find({'userId': $routeParams.id},
            function(res){
                 $scope.friend_relationship = res.data[0]
            }, function(err){
                console.log(err);
            }
        );

        console.log("FriendCtl");
    }

    angular.module("app").controller('FriendCrtl', FriendCrtl);
})();