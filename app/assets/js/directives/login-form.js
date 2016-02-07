(function() {
    function loginForm() {
        return {
            restrict: "E",
            replace: true,
            templateUrl: "/static/partials/directives/login-form.html",
            scope: {

            },
            controller: 'LoginCtrl',
            link: function($scope, $element, $attrs) {


            }
        }

    }

    angular.module("app").directive("loginForm", loginForm);
})();
