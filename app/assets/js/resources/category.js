(function() {
    angular.module("app").factory('CategoryService',  function postResource($resource) {
        return $resource("/v1/api/Category/:id", {id:'@id'}, {
            "find_all": {
                method: "GET",
            }
        });
    });
})();
