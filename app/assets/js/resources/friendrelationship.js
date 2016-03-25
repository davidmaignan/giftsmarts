(function() {
    angular.module("app").factory('FriendRelationshipService',  function postResource($resource) {
        return $resource("/v1/api/FriendRelationship/:userId", {userId:'@userId'}, {
            "find_all": {
                method: "GET"
            },
            "find": {
                method: "GET"
            }
        });
    });

    angular.module("app").factory('FriendRelationshipTypeService', function postResource($resource) {
        return $resource("/v1/api/FriendRelationshipType/", null, {
            "find_all": {
                method: "GET"
            }
        })
    });
})();
