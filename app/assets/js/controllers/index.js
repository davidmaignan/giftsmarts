(function(){
    "use strict";
    function IndexCtrl($scope, $timeout, $document, FriendRelationshipService, FriendRelationshipTypeService, filterFilter) {

        $scope.friend_relationships;
        $scope.filter_friend_relationships;

        FriendRelationshipTypeService.find_all({},
            function(res){
                $scope.relationship_types = res.data
            }, function(err){
                console.log(err)
            }
        );

        FriendRelationshipService.find_all({},
            function(res){
                $scope.friend_relationships = res.data;
                $scope.filter_friend_relationships = res.data;
                console.log(res);
            }, function(err){
                console.error(err);
            });

        $scope.isRelationshipType = function(value1, value2){
            return value1 == value2;
        };

        $scope.setRelationshipType = function(relationship, relationshipType) {
            var relationshipObj  = { "data": {
                                        "entity": "FriendRelationship",
                                        "id": relationship.id,
                                        "owner_id": relationship.owner_id,
                                        "friend_id": relationship.friend_id,
                                        "relation_type": relationshipType,
                                        "active": 0
                                        }
                                    }

            FriendRelationshipService.put({}, relationshipObj, function(res){
                relationship.relationship_type = res.data[0].relationship_type;
                relationship.relationship = res.data[0].relationship;
                $timeout(isotopeArrange, 500, true, relationship.id, relationshipType);
            }, function(err){
                console.error(err);
            });
        };

        $scope.searchFriend = function (value) {
            $scope.filter_friend_relationships = filterFilter($scope.friend_relationships, function(data) {
                if (data.to_friend.name.toLowerCase().indexOf(value.toLowerCase()) != -1){
                    return true;
                }

                return false;
            });
            $timeout(isotopeReArrange, 500, true);
        }

        $scope.setRelationshipIcon = function (value) {
            if(value == 1) {
                return "glyphicon-heart";
            } else if (value == 2){
                return "glyphicon-heart-empty";
            } else if (value == 3) {
                return "glyphicon-user";
            }else {
                return "glyphicon-compressed";
            }
        }
    }

    function setButtonStatus(id, type) {
        var buttons = $(".relationship-" + id);
        for(var i = 0; i < buttons.length; i++)
            buttons[i].disabled = (type == (i+1))? true: false;
    }

    function isotopeArrange(relationshipId, relationshipType){
        var s = angular.element('#isotopeContainer').scope();
        s.$emit('iso-method', {name:'arrange'});
        setButtonStatus(relationshipId, relationshipType)
    }

    function isotopeReArrange(){
        var s = angular.element('#isotopeContainer').scope();
        s.$emit('iso-method', {name:'arrange'});
    }

    angular.module("app").controller('IndexCtrl', IndexCtrl);
})();