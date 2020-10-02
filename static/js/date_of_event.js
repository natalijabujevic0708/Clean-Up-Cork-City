// Create a list that contains the dates of all the Saturdays starting from today

function generateSaturdays() {
    var today = new Date();
    var year = today.getFullYear();
    var month = today.getMonth();
    var day = today.getDate();
    var date_of_cleanup = document.getElementsByClassName("date_of_cleanup");
    var saturdays = [];
    var i = 0;
    var l = 0;

    while (i < date_of_cleanup.length) {

        var date = new Date(year, month, day + l);

        if (date.getDay() == 6) {
            datestring = date.getDate() + "-" + (date.getMonth() + 1) + "-" + date.getFullYear();
            saturdays.push(datestring);
            date_of_cleanup[i].innerHTML = saturdays[i]
            i++;
        }
        l++
    }
}
generateSaturdays();

