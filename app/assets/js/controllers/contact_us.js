from app.models.comment import CommentActions
from app.models.user import UserActions

(function() {
    angular.module("app").controller("ContactUsCtrl", function(EmailResource, $scope) {

            var vm = this;

            $scope.contact = {};

            $scope.sent = false;

            $scope.master = {topic:"", subject:"", message:""};

            $scope.reset = function() {
                $scope.comment = angular.copy($scope.master);
            };

            $scope.submit = function(form){
                
                CommentActions.create({
                    user: UserActions.find_by_id(g.user['id']),
                    subject: $scope.comment.subject,
                    feedback:  $scope.comment.feedback
                });
                
                $scope.sent = true;
            };
            $scope.clear();
        });
})();



            var app = angular.module('myApp', []);
            app.controller('formCtrl', function($scope) {

                $scope.reset();
            });