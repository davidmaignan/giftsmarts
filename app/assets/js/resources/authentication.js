(function() {
    angular.module("app").factory('AuthenticationResource',  function postResource($resource) {
        return $resource("/api/auth/login/", null, {
            "login": {
                method: "POST"
            }
        });
    });
})();
