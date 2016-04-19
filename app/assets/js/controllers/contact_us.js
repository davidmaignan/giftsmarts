(function() {
    angular.module("app").controller("ContactUsCtrl", function(ConctactResource, $scope) {

            var vm = this;

            $scope.contact = {};

            $scope.sent = false;

            $scope.master = {topic:"", subject:"", message:""};

            $scope.reset = function() {
                $scope.comment = angular.copy($scope.master);
            };

            $scope.submit = function(){
                
                var userContactObj = {"data": {
                    "subject": $scope.comment.subject,
                    "feedback": $scope.comment.feedback
                }
                };

                ConctactResource.post_comment();

                $scope.sent = true;
            };
            $scope.clear();
        });
})();



            var app = angular.module('myApp', []);
            app.controller('formCtrl', function($scope) {

                $scope.reset();
            });