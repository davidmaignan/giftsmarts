(function() {
    angular.module("app").factory('FriendRelationshipService',  function postResource($resource) {
        return $resource("/v1/api/FriendRelationship/:userId/", {userId:'@userId'}, {
            "find_all": {
                method: "GET"
            },
            "find": {
                method: "GET"
            },
            "put": {
                method: "PUT",
                headers: {
                    "Accept" : "application/json",
                    "Content-Type" : "application/json"
                }
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

    angular.module("app").factory('PutService', function postResource($resource) {
        return $resource("/v1/api", null, {
            "send": {
                method: "PUT",
                headers: {
                    "Accept" : "application/json",
                    "Content-Type" : "application/json"
                }
            }
        })
    });
})();
