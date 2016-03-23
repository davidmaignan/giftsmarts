(function() {
    angular.module("app").factory('FriendRelationshipService',  function postResource($resource) {
        return $resource("/v1/api/FriendRelationship/", null, {
            "find_all": {
                method: "GET"
            }
        });
    });
})();
