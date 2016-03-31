(function() {
    angular.module("app").factory('AmazonService',  function postResource($resource) {
        return $resource("/amazon/fetch-products/:userId/", {userId:'@userId', taskId: '@taskId'}, {
            "fetchProducts": {
                method: "GET"
            },
            "progressStatus": {
                method: 'GET',
                url: '/amazon/status/:taskId/'
            },
        });
    });
})();