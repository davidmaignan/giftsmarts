(function() {
    "use strict";

    function httpInterceptor($rootScope, $q, $window) {
        return {
            request: function(request) {
                if ($rootScope.$storage.token) {
                    request.headers.Authorization = "Bearer " + $rootScope.$storage.token;
                }
                return request;
            },
            response: function(response) {
                var headers = response.headers(); 

                if(headers.token) {
                    var token = headers.token.split("Bearer ")[1];
                    
                    if(!$rootScope.$storage.token) {
                        $rootScope.$storage.token = token;
                    } else {
                        var expiration = moment(JSON.parse(atob($rootScope.$storage.token.split(".")[1]))["expiration"]);
                        var new_expiration = moment(JSON.parse(atob(token.split(".")[1]))["expiration"]);

                        if(new_expiration > expiration) {
                            $rootScope.$storage.token = token;
                        }
                    }
                }

                return response;
            },
            responseError: function(response) {
                if (response.status == 403) {
                    $rootScope.$storage.token = undefined;
                    $window.location = '/login';
                }

                return $q.reject(response);
            }
        };
    }

    angular.module("app").factory('httpInterceptor', httpInterceptor);
})();
