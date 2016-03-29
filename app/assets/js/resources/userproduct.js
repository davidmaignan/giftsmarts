(function() {
    angular.module("app").factory('UserProductService',  function postResource($resource) {
        return $resource("/v1/api/UserProduct/:userId", {userId:'@userId'}, {
            "find_all": {
                method: "GET",
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
})();
