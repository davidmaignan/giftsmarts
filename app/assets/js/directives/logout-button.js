(function() {
    function logoutButton() {
        return {
            restrict: "E",
            replace: true,
            templateUrl: "/static/partials/directives/logout-button.html",
            scope: {},
            controller: 'LogoutCtrl'
        }
    }

    angular.module("app").directive("logoutButton", logoutButton);
})();
