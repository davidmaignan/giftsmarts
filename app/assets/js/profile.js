(function() {
    "use strict";

    var $container;

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

    $(document).ready(execute);

    function activateProductDetailLink() {
         $('.product-title-link').click(function (e){
            document.location.href="#top";
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
    }

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

        $('.btn-close').click(function() {
            $('#main').show();
            $('#product-detail').hide();
        });

        var task_id = $('#task-id').attr('data') || null;
        var template = function(imageURL, title, author, price){
            var html_tpl = '<div class="box grid-item"><img src="' + imageURL +'" /> ' +
                            '<h4><a href="#" class="product-title-link">' + title +
                            '</a></h4>' +
                            '<p class="author">by:  ' + author +
                            '</p>' +
                            '<p>category, keyword 1, keyword 2</p>' +
                            '<p>Price: <span class="price">' + price + '</span>' +
                            '</p><p>' +
                                '<a href="#" class="btn btn-default"><span class="glyphicon glyphicon-thumbs-down"</span></a>' +
                                '<a href="#" class="btn btn-success"><span class="glyphicon glyphicon-thumbs-up"</span></a>' +
                            '</p></div>'

            return html_tpl;
        };

        var success = false;
        var productTask = function() {
            $.getJSON('/status/' + task_id, function(data) {
                if(data.state === "SUCCESS" && success === false) {
                        $('#progress-status').html(100 + '% completed');

                        success = true;
                        $( "#main" ).empty();

                        //Stop ajax
                        clearInterval(productTaskRefresh);

                         var i = 0, total = data.products.length;

                         for(i = 0; i < total; i++){
                            var product = data.products[i];
                            var title, imageURL, author, price;

                            if(product.Item.hasOwnProperty("ItemAttributes")) {
                                title = product.Item.ItemAttributes.Title;
                                author = product.Item.ItemAttributes.Author;

                                if(product.Item.ItemAttributes.hasOwnProperty("ListPrice")) {
                                    price = product.Item.ItemAttributes.ListPrice.FormattedPrice;
                                }
                            }

                            if(product.Item.hasOwnProperty("MediumImage")) {
                                imageURL = product.Item.MediumImage.URL;
                            }

                            var tpl = template(imageURL, title, author, price);
                            var $tpl = $(tpl).attr('data', JSON.stringify(product));

                            $('#main').append($tpl);
                         }

                        var $grid = $('#main').packery({
                            itemSelector: '.box',
                            gutter: 30
                        });

                        activateProductDetailLink();

                } else if (data.state === "FAILURE"){
                    $("#main" ).empty();
                    $('#main').append("<h4>An error has occured. Please try again !</h4>");
                    clearInterval(productTaskRefresh);
                } else if (data.state === "PROGRESS") {
                    var percent = data.current / data.total * 100;

                    $('#progress-status').html(percent + '% completed');

                    console.log(data);
                }
            });
        };

        if(task_id !== null) {
             var productTaskRefresh = setInterval(productTask, 1000);
        }
    }
})($, Isotope);