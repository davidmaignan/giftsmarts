(function() {
    "use strict";

    function run($rootScope, $localStorage, $http) {

        $rootScope.$storage = $localStorage;
        
    }

    angular.module("app")
        .run(run);
})();
