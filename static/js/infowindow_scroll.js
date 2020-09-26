// Click on the infowindow brings you to the article containing details
function search_address(){
    var address = document.getElementById("search_address").innerHTML
    var list= document.getElementsByClassName("address");
    for (var i = 0; i < list.length; i++) {
        if (list[i].innerHTML == address){
            list[i].scrollIntoView()
        }
    }
}