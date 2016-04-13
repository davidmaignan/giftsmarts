(function() {
    angular.module("app").factory('UserCategoryService',  function postResource($resource) {
        return $resource("/v1/api/UserCategory/:userId", {userId:'@userId'}, {
            "find_by_user": {
                method: "GET",
            }
        });
    });
})();
