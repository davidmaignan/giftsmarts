(function(){
    "use strict";
    function IndexCtrl($scope, FriendRelationshipService, FriendRelationshipTypeService) {

        FriendRelationshipTypeService.find_all({},
            function(res){
                $scope.relationship_types = res.data
            }, function(err){
                console.log(err)
            }
        );

        FriendRelationshipService.find_all({},
            function(res){
                $scope.friend_relationships = res.data
                console.log(res);
            }, function(err){
                console.error(err);
            });
    }

    angular.module("app").controller('IndexCtrl', IndexCtrl);
})();