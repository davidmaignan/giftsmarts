(function() {
    angular.module("app").factory('ConctactResource',  function postResource($resource) {
        return $resource("/v1/api/ContactUs/", null, {
            "post_comment": {
                method: "POST"
            }
        });
    });
})();
