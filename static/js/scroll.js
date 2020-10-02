// Scroll animation on index.html

$(document).ready(function () {
    $("#scroll_link").click(function () {
        $('html, body').animate({
            scrollTop: $("#main").offset().top
        }, 1000);
    });
});