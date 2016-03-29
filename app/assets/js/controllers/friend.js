(function(){
    "use strict";
    function FriendCrtl($scope, $routeParams, UserProductService, FriendRelationshipService, CategoryService, AmazonReviewService, $timeout) {
        console.log("FriendCrtl" + $routeParams.id);

        $scope.productDetail = "";
        $scope.productReview = "";

        UserProductService.find_all({'userId': $routeParams.id, 'active': 1},
            function(res){
                $scope.userProducts = res.data
                console.log(res.data);
            }, function(err){
                console.log(err);
            }
        );

        CategoryService.find_all({},
            function(res) {
                $scope.categories = res.data
            }, function(err){
                console.log(err);
            }
        );

        FriendRelationshipService.find({'userId': $routeParams.id},
            function(res){
                 $scope.friend_relationship = res.data[0]
                 console.log(res.data[0]);
            }, function(err){
                console.log(err);
            }
        );

        $scope.showDetails = function (userProduct) {
            $scope.productDetail = userProduct.product_details;
            $('#isotopeContainer').hide();
            $('#product-detail').removeClass('hide').show();

            var customerReviewsURL = userProduct.product_details.Item.CustomerReviews.IFrameURL;
            var url = encodeURI(customerReviewsURL);

            AmazonReviewService.get({},
                function(res){
                    console.log(res);
                }, function(err){
                    console.log(err);
                }
            );

            console.log(url);

        };

        $scope.hideDetails = function(){
            $('#isotopeContainer').show();
            $('#product-detail').hide();
        };

        $scope.reject = function (userProduct) {
            console.log(userProduct);

            var userProductObj = {"data": {
                    "entity": "UserProduct",
                    "user_id": userProduct.user_id,
                    "product_id": userProduct.product_id,
                    "category_id": userProduct.category_id,
                    "active": 0
                }
            };

            UserProductService.put({}, userProductObj, function(res){
                    userProduct.active = 0;
                    console.log(res);
                    var index = $scope.userProducts.indexOf(userProduct);
                    console.log(index);
                    $scope.userProducts.splice(index, 1);
                    $timeout(isotopeArrange, 100, true);
                }, function(err){
                console.error(err);
            });
        };
    }

    function isotopeArrange(relationshipId, relationshipType){
        var s=angular.element('#isotopeContainer').scope();
        s.$emit('iso-method', {name:'arrange'});
    }

    angular.module("app").controller('FriendCrtl', FriendCrtl);
})();