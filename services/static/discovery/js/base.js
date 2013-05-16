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
    var clip = new ZeroClipboard( document.getElementById("copy"), {
        moviePath: "http://worker.101companies.org/services/static/discovery/swf/libs/ZeroClipboard.swf",
        trustedDomains: ['*'],
        allowScriptAccess: "always"
    });

    var clip2 = new ZeroClipboard( document.getElementById("copy-relative"), {
        moviePath: "http://worker.101companies.org/services/static/discovery/swf/libs/ZeroClipboard.swf",
        trustedDomains: ['*'],
        allowScriptAccess: "always"
    });

    var clip3 = new ZeroClipboard( document.getElementById("copy-markup"), {
        moviePath: "http://worker.101companies.org/services/static/discovery/swf/libs/ZeroClipboard.swf",
        trustedDomains: ['*'],
        allowScriptAccess: "always"
    });
}