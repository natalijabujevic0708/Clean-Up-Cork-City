// To retain the scroll position of a scrollable area when pressing the back button

$(function () {
    var pathName = document.location.pathname;
    window.onbeforeunload = function () {
        var scrollPosition = $(document).scrollTop();
        sessionStorage.setItem("scrollPosition_" + pathName, scrollPosition.toString());
        
    };
    if (sessionStorage["scrollPosition_" + pathName]) {
        $(document).scrollTop(sessionStorage.getItem("scrollPosition_" + pathName));
    }
});
// When a user clicks the button "Add a new location" on their profile page, set the value of the forms position to the session storage for the locations page, so that the user is redirected there
function go_to_form(){
    sessionStorage.setItem("scrollPosition_/locations", "1800"); 
}
