(function() {
    "use strict";

    function config($httpProvider) {
        $httpProvider.interceptors.push("httpInterceptor");
    }

    angular.module("app")
        .config(config);
})();
