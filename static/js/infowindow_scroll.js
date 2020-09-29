// Click on the info window brings you to the article containing the details abot the location
function search_address(){
    var address = document.getElementById("search_address").innerHTML
    var list= document.getElementsByClassName("address");
    for (var i = 0; i < list.length; i++) {
        if (list[i].innerHTML == address){
            list[i].scrollIntoView()
        }
    }
}