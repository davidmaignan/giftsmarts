(function() {
    angular.module("app").factory('UserResource',  function postResource($resource) {
        return $resource("/api/user/username", null, {
            "get_username": {
                method: "GET"
            }
        });
    });
})();
