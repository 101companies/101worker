$(document).ready(function(){
    init_masonry();
    
    var afterCopyCallback = function(){
        var targetId = $(this).attr('data-clipboard-target');
        var targetText = document.getElementById(targetId).innerText;
        $('#locator').popover({trigger: 'manual', placement: 'bottom', content: 'copied data into clipboard'});
        $('#locator').popover('show');
        setTimeout(function() {
            $('#locator').popover('hide');
        }, 2000);
    };
    
    var copyCallback = function(){
        var targetId = $(this).attr('data-clipboard-target');
        return document.getElementById(targetId).innerText;
    }

    //normal copy button
    $('#copy').zclip({
        path:'http://www.steamdev.com/zclip/js/ZeroClipboard.swf',
        copy: copyCallback,
        afterCopy: afterCopyCallback
    })

    //necessary for dropdowns
    function addZClip () {
        $('.copy').each(function(){
            if($(this).is(':visible')){
                $(this).zclip({
                    path:'http://www.steamdev.com/zclip/js/ZeroClipboard.swf',
                    copy: copyCallback,
                    // remove hover class after clicking the element
                    beforeCopy: function(){
                        $(this).removeClass('hover');
                    },
                    afterCopy: afterCopyCallback
                });
                clearInterval(check);
            }
        });
    }

    var check = setInterval(addZClip, 100);
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
