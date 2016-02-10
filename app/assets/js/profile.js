(function() {
    "use strict";
    var $container;

    $(document).ready(execute);

    function execute(){
    	$container = $('#container');
		$container.packery({
		  itemSelector: '.item',
		  gutter: 10
		});
    }
})($);