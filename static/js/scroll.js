$(document).ready(function() {
    $("#scrollLink").click(function() {
        $('html, body').animate({
            scrollTop: $("#main").offset().top
        }, 1000);
    });
});