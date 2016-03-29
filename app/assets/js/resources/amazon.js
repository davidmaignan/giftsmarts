(function() {
    angular.module("app").factory('AmazonReviewService',  function postResource($resource) {
        return $resource("/amazon/customer-review/:url/", {url:'@url'}, {
            "get": {
                method: "GET"
            }
        });
    });
})();