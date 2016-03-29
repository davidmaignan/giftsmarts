(function(){
    "use strict";
    function IndexCtrl($scope, $timeout, $document, FriendRelationshipService, FriendRelationshipTypeService, PutService) {
        FriendRelationshipTypeService.find_all({},
            function(res){
                $scope.relationship_types = res.data
            }, function(err){
                console.log(err)
            }
        );

        FriendRelationshipService.find_all({},
            function(res){
                $scope.friend_relationships = res.data
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
    }

    function setButtonStatus(id, type) {
        var buttons = $(".relationship-" + id);
        for(var i = 0; i < buttons.length; i++)
            buttons[i].disabled = (type == (i+1))? true: false;
    }

    function isotopeArrange(relationshipId, relationshipType){
        var s=angular.element('#isotopeContainer').scope();
        s.$emit('iso-method', {name:'arrange'});
        setButtonStatus(relationshipId, relationshipType)
    }

    angular.module("app").controller('IndexCtrl', IndexCtrl);
})();