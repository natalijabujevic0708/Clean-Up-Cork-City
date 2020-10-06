$(document).ready(function () {
    if ($('#uploaded_locations').length) {
        $("#title").html("The locations you uploaded:");
    }else {
        $("#title").html("Upload your first location<br>or<br> join us for a cleanup event!");
    };
});