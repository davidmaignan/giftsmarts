(function(){
    "use strict";
    function FriendCrtl($scope, $routeParams, UserProductService, FriendRelationshipService, CategoryService, AmazonService, $timeout) {
        $scope.productDetail = "";
        $scope.friendId = $routeParams.id
        $scope.taskId;
        $scope.progressValue = 3;
        $scope.userProducts = [];
        $scope.maxRequests = 11;
        $scope.totalRequests = 0;

        UserProductService.find_all({'userId': $routeParams.id, 'active': 1},
            function(res){
                $scope.userProducts = res.data;

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

        function checkProgressUpdate()
        {
            if($scope.taskId !== null) {
                AmazonService.progressStatus({'taskId': $scope.taskId},
                    function(res){
                        console.log(res);
                        $scope.progressValue = parseInt(res.current / res.total * 100);
                        $scope.totalRequests++;

                        if(res.state === "PROGRESS" || res.state === "PENDING"){

                            if ($scope.maxRequests > $scope.totalRequests){
                                $timeout(checkProgressUpdate, 1000, true);
                            }

                            if(res.hasOwnProperty('data') === true){
                                for(var elt in res.data){
                                    if ($scope.userProducts.indexOf(res.data[elt]) == -1) {
                                         $scope.userProducts.push(res.data[elt]);
                                     }
                                }
                            }
                        } else if (res.state === "FAILURE"){
                            console.log("FAILURE TO FIX")
                        } else if (res.state === "SUCCESS") {
                            if(res.hasOwnProperty('data') === true){
                                for(var elt in res.data){
                                    if ($scope.userProducts.indexOf(res.data[elt]) == -1) {
                                         $scope.userProducts.push(res.data[elt]);
                                     }
                                }
                            }
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