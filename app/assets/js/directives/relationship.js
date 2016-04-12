(function() {
    function relationshipIcon() {
      return {
          restrict: 'AE',
          replace: 'true',
          templateUrl: "/static/partials/directives/friend-relationship.html",
          scope: {
              type: "@type",
              relationship: "@relationship"
            }
      };
    }

    angular.module("app").directive("friendRelationship", relationshipIcon);
})();
