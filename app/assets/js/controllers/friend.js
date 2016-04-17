(function(){
    "use strict";
    function FriendCrtl($scope, $routeParams, UserProductService, FriendRelationshipService, CategoryService, AmazonService,
                        UserCategoryService,$timeout) {
        $scope.productDetail = "";
        $scope.friendId = $routeParams.id
        $scope.taskId;
        $scope.progressValue = 3;
        $scope.userProducts = [];
        $scope.userProductIds = [];
        $scope.maxRequests = 11;
        $scope.totalRequests = 0;
        $scope.categories = [];
        $scope.categoryIds = [];
        $scope.wishListTotal = 0;

        UserProductService.find_all({'userId': $routeParams.id, 'active': 1},
            function(res){
                addUserProduct(res);
                addCategory(res);

                if($scope.userProducts.length === 0) {
                    AmazonService.fetchProducts({'userId': $scope.friendId},
                        function(res){
                            $scope.taskId = res.data.task_id;
                            checkProgressUpdate();

                            console.log(res)
                        }, function(err){
                            console.log(err);
                        }
                    );
                } else{
                    $('#progress-control').slideUp('slow');
                }
            }, function(err){
                console.log(err);
            }
        );

        function addUserProduct(res){
            if(res.hasOwnProperty('data')){
                for(var elt in res.data){
                    if ($scope.userProductIds.indexOf(res.data[elt].product_id) === -1) {
                        $scope.userProductIds.push(res.data[elt].product_id);
                        $scope.userProducts.push(res.data[elt]);

                        if(res.data[elt].wish_list) {
                            $scope.wishListTotal++;
                        }
                     }
                }
            }
        }

        function addCategory(res){
            if(res.hasOwnProperty('data')) {
                for(var product in res.data){
                    if(res.data[product].hasOwnProperty('category')){
                        if($scope.categoryIds.indexOf(res.data[product].category_id) === -1){
                            $scope.categoryIds.push(res.data[product].category_id);
                            $scope.categories.push(res.data[product].category);
                        }
                    }
                }
            }
        }

        function checkProgressUpdate()
        {
            if($scope.taskId !== null) {
                AmazonService.progressStatus({'taskId': $scope.taskId},
                    function(res){
                        console.log('Res rpogress status', res);

                        var floatingValue = 0;

                        if (res.current && res.total) {
                            floatingValue = res.current / res.total;
                        }

                        $scope.progressValue = parseInt(floatingValue * 100);
                        $scope.totalRequests++;

                        if(res.state === "PROGRESS" || res.state === "PENDING"){

                            if ($scope.maxRequests > $scope.totalRequests){
                                $timeout(checkProgressUpdate, 1000, true);
                            }

                            addUserProduct(res);

                            addCategory(res);

                        } else if (res.state === "FAILURE"){
                            console.log("FAILURE TO FIX")
                        } else if (res.state === "SUCCESS") {
                            addUserProduct(res);

                            $('#progress-control').hide('slow');
                        } else {
                            console.log(res);
                        }

                    }, function(err){
                        console.log(err);
                    }
                );
            }
        }

        FriendRelationshipService.find({'userId': $routeParams.id},
            function(res){
                 $scope.friend_relationship = res.data[0]
            }, function(err){
                console.log(err);
            }
        );

        $scope.showDetails = function (userProduct) {
            $scope.productDetail = userProduct.product_details;
            $('#isotopeContainer').hide();
            $('#product-detail').removeClass('hide').show();
            $('#amazon-user-reviews').attr('src', $scope.productDetail.Item.CustomerReviews.IFrameURL);
        };

        $scope.hideDetails = function(){
            $('#isotopeContainer').show();
            $('#product-detail').hide();
        };

        $scope.accept = function(userProduct) {
            var userProductObj = {"data": {
                    "entity": "UserProduct",
                    "user_id": userProduct.user_id,
                    "product_id": userProduct.product_id,
                    "category_id": userProduct.category_id,
                    "wish_list": 1,
                    "active": 1
                }
            };

            UserProductService.put({}, userProductObj, function(res){
                console.log(res);
                $scope.wishListTotal++;
                }, function(err){
                console.error(err);
            });

        }

        $scope.reject = function (userProduct) {
            var userProductObj = {"data": {
                    "entity": "UserProduct",
                    "user_id": userProduct.user_id,
                    "product_id": userProduct.product_id,
                    "category_id": userProduct.category_id,
                    "wish_list": userProduct.wish_list,
                    "active": 0
                }
            };

            UserProductService.put({}, userProductObj, function(res){
                    userProduct.active = 0;
                    var index = $scope.userProducts.indexOf(userProduct);
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
