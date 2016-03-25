(function() {
    "use strict";

    function run($rootScope, $localStorage, $http, $templateCache) {
        $rootScope.$storage = $localStorage;
        $rootScope.$on('$viewContentLoaded', function() {
          $templateCache.removeAll();
       });
    }

    var module = angular.module("app");

    module.filter('slug', function(){
        return function(input){
            if(input)
                return input.toLowerCase().replace(' ', '_');
        };
    });

    module.filter('ucwords', function(){
        return function(input){
            return (input + '')
                .replace(/^([a-z\u00E0-\u00FC])|\s+([a-z\u00E0-\u00FC])/g, function($1) {
                return $1.toUpperCase();
            });
        };
    });

    module.run(run);
})();
