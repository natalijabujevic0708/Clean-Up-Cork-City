// To retain the scroll position of a scrollable area when pressing the back button

$(function () {
    var pathName = document.location.pathname;
    window.onbeforeunload = function () {
        var scrollPosition = $(document).scrollTop();
        sessionStorage.setItem("scrollPosition_" + pathName, scrollPosition.toString());
        
    }
    if (sessionStorage["scrollPosition_" + pathName]) {
        $(document).scrollTop(sessionStorage.getItem("scrollPosition_" + pathName));
    }
});
function go_to_form(){
    sessionStorage.setItem("scrollPosition_/locations", "1800"); // to go back to the form
}