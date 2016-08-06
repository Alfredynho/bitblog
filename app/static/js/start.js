$(document).ready(function() {
    $(".owl-slider").owlCarousel({

        autoPlay: 3000, //Set AutoPlay to 3 seconds
        items : 4,
        itemsDesktop : [1199,3],
        itemsDesktopSmall : [979,3],
        navigation : true,
        navigationText:	["ANTERIOR","SIGUIENTE"],
        pagination: false
    });

    var $socialBlocks = $("[data-entry-url]");


    $.each($socialBlocks, function(index, item){
        var url = 'http://' + location.host + $(item).attr("data-entry-url");
        var title = $(item).attr("data-entry-title");

        console.log(url, title);

        $(item).jsSocials({
            shares: ["facebook", "twitter", "googleplus", "email"],
            url: url,
            text: title,
            shareIn: "popup",
            showLabel: false
        });
    });


});



