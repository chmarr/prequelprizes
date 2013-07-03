(function($, name) {
/* jQuery typewriter plugin
    2012-11-15
    https://github.com/bergus */
    $[name+"Defaults"] = {
        framerate: 1000/60,
        group: /.{0,2}/g // 2: Number of chars per frame
    };
    $.fn[name] = function(options, callback) {
        if (typeof options != 'object') callback=options, options={};

        return this.each(function() {
            var el = $(this),
                conf = $.extend({}, $[name+"Defaults"], options);
            el.queue("fx", function(next) {
                animateNode(this, conf, typeof callback == 'function'
                  ? function() { callback.call(el[0]); next(); }
                  : next
                );
                el.show();
            });
        });
    };
    function chunk(text, conf) {
        // splitting the text into parts (http://stackoverflow.com/a/11657799/1048572)
        return text.match(conf.group);
    }
    function timeout(callback, conf) {
        // set up the timeout
        // want to randomize? Have a look at http://jsfiddle.net/pZb8W/2/ for possible implementation
        setTimeout(callback, conf.framerate);
    }
    function animateNode(element, conf, callback) {
        var pieces = [];
        if (element.nodeType==1 && element.hasChildNodes()) {
            while (element.hasChildNodes())
                pieces.push(element.removeChild(element.firstChild));
            timeout(function childStep() {
                if (pieces.length) {
                    var piece = pieces.shift();
                    animateNode(piece, conf, childStep);
                    element.appendChild(piece);
                } else
                    callback();
            }, conf);
        } else if (element.nodeType==3) {
            pieces = chunk(element.data, conf);
            element.data = "";
            (function addText(){
                element.data += pieces.shift();
                timeout(pieces.length ? addText : callback, conf);
            })();
        } else // empty or special (comment etc) node
            timeout(callback, conf);
    }

})(jQuery, "typewriter");
