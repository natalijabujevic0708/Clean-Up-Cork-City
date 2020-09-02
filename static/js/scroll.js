$(document).ready(function() {
    $("#scrollLink").click(function() {
        $('html, body').animate({
            scrollTop: $("#main").offset().top
        }, 1000);
    });
    $("#scrollLinkMap").click(function() {
        $('html, body').animate({
            scrollTop: $("#map").offset().top
        }, 1000);
    });
    $("#scrollLinkForm").click(function() {
        $('html, body').animate({
            scrollTop: $("#addressForm").offset().top
        }, 1000);
    });
});