(function() {
    "use strict";

    function config($httpProvider, $resourceProvider) {
        $httpProvider.interceptors.push("httpInterceptor");
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }

    angular.module("app")
        .config(config);
})();