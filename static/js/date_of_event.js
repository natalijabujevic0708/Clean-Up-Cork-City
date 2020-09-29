// Create a list that contains the dates of all the Saturdays starting from today
var today = new Date();
var year = today.getFullYear()
var month = today.getMonth()
var day = today.getDate();

var saturdays = [];

for (var i = 0; i <= new Date(year, month, day).getDate(); i++) 
{    
    var date = new Date(year, month, day + i);

    if (date.getDay() == 6)
    {
        datestring = date.getDate()  + "-" + (date.getMonth()+1) + "-" + date.getFullYear()
        saturdays.push(datestring);
    } 
   
};
// Add the dates to the events
var date_of_cleanup = document.getElementsByClassName("date_of_cleanup");
for (var i = 0; i < date_of_cleanup.length; i++) {
    date_of_cleanup[i].innerHTML = saturdays[i]
}

