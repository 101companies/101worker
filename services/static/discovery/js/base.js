$(document).ready(function(){
    init_masonry();

    init_ZeroClipboard();
});

function init_masonry(){
    var $container = $('#content');
    $container.masonry({
        itemSelector: '.box',
        isAnimated: true,
        columnWidth: function( containerWidth ) {
            // do nothing for browsers with no media query support
            // .container will always be 940px
            if($(".container").width() == 940) {
                return 240;
            }
            var width = $(window).width();
            var col = 300;
            if(width < 1200 && width >= 980) {
                col = 240;
            }
            else if(width < 980 && width >= 768) {
                col = 186;
            }
            return col;
        }
    });
}
function init_ZeroClipboard() {
    var clip = new ZeroClipboard( document.getElementById("copy-button"), {
        moviePath: "http://localhost/services/static/discovery/swf/libs/ZeroClipboard.swf"
        //moviePath: "http://worker.101companies.org/services/static/discovery/swf/libs/ZeroClipboard.swf"
    });

    clip.on( 'load', function(client) {
        // alert( "movie is loaded" );
    } );

    clip.on( 'complete', function(client, args) {
        //alert('copied into clipboard')
        //document.getElementById('copy-button').addClass('btn-success')
    } );
}