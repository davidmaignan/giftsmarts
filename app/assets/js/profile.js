(function() {
    "use strict";

    //substr so there isn't a '#'
    var hashFilter = location.hash.substr(1);

    var mainEl = $('#main');
    var transitionDuration = 800;
    var columnWidth = 270;

    mainEl.isotope({
        filter: hashFilter,
        animationEngine: 'best-available', //CSS3 if browser supports it, jQuery otherwise
        animationOptions: {
            duration: transitionDuration
        },
        containerStyle: {
            position: 'relative',
            overflow: 'visible'
        },
        masonry: {
            columnWidth: columnWidth
        }
    });


    function setSizes(){
        var availableSpace = $(window).width();
        var potentialColumns = availableSpace/columnWidth;
        potentialColumns = Math.floor(potentialColumns);

        var newWidth = potentialColumns * columnWidth;

        $('.container').width(newWidth - 300);
    }

    setSizes();

    function layoutTimer(){
        setTimeout(function(){
            mainEl.isotope('layout');
        }, transitionDuration);
    }

    layoutTimer();

    $(window).resize(function(){
        setSizes();
        layoutTimer();
    });


    var currentCats = hashFilter.split(".");
    //splice because the first element will be just an empty '', so we get rid of it
    currentCats.splice(0, 1);

    for (current in currentCats){
        currentCat = currentCats[current];

        //Since it splices based on the '.', each '.' disappears, so we need to re-add it
        currentCats[current] = '.' + currentCat;

        //Find each link that has a 'href' attribute currently present in the hash
        $('#controls a[href=#'+currentCat+']').parent().addClass('active');

    }

//    $('#controls a').click(function(){
//        //Change '#cat1' into '.cat1'
//        var catClass = '.'+$(this).attr('href').substr(1);
//
//        //If the current category is not in the array, add it and make the link active
//        if($.inArray(catClass, currentCats)==-1){
//            currentCats.push(catClass);
//            $(this).parent().addClass('active');
//        }
//        //If the current category is in the array, get rid of it and remove the 'active' class
//        else {
//            //position of the current category in the array
//            position = $.inArray(catClass, currentCats);
//            currentCats.splice(position,1);
//            $(this).parent().removeClass('active');
//        }
//
//        var newFilter = "";
//
//        //generate a 'newFilter' string that will be saved into the hash
//        for (current in currentCats){
//            currentCat = currentCats[current];
//            newFilter = newFilter + currentCat;
//        }
//
//        location.hash = newFilter;
//
//        mainEl.isotope({
//            filter: newFilter
//        });
//
//        return false;
//
//    });

    var $container;

    $(document).ready(execute);

    function execute(){
        $container = $('#container');
        $container.packery({
          itemSelector: '.box',
          gutter: 10
        });

        // filter items on button click
        $filterButton = $('.filter-button-group > button');

        var $filterButton = $('.filter-button-group > button');

        $('.filter-button-group > button').on( 'click', function() {
            $filterButton.removeClass('active');
            $(this).addClass('active');
            var filterValue = $(this).attr('data-filter');
            mainEl.isotope({ filter: filterValue });
        });

        $('.product-title-link').click(function (e){
            e.preventDefault();
             var data_str = $(this).closest('.grid-item').attr('data');
             var data_json = jQuery.parseJSON(data_str);

             $('#product-detail-image').attr('src', data_json.Item.LargeImage.URL);
             $('#product-detail-title').html(data_json.Item.ItemAttributes.Title);
             $('#product-detail-author').html(data_json.Item.ItemAttributes.Author);
             $('#product-detail-label').html(data_json.Item.ItemAttributes.Label);
             $('#product-detail-number-pages').html(data_json.Item.ItemAttributes.NumberOfPages);
             $('#product-detail-release-date').html(data_json.Item.ItemAttributes.ReleaseDate);
             $('#product-detail-price').html(data_json.Item.ItemAttributes.ListPrice.FormattedPrice);
             $('#product-detail-description').html(data_json.Item.EditorialReviews.EditorialReview.Content);
             $('#amazon-user-reviews').attr('src', data_json.Item.CustomerReviews.IFrameURL);

             $('#main').hide();
             $('#product-detail').removeClass('hide').show();
         });

        $('.btn-close').click(function() {
            $('#main').show();
            $('#product-detail').hide();
        });
    }
})($, Isotope);