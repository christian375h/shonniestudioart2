const counters = ["facePaintCounter", "glitterTattoosCounter", "paintNightCounter"];

const choices = ["facePaint", "glitterTattoos", "paintNight"];

function setFace(){
    setChoice(0);
}
function setTattoo(){
    setChoice(1);
}
function setNight(){
    setChoice(2);
}

let dateTime = document.getElementById('contact-info-form');
dateTime.addEventListener("submit", (e) => {
    e.preventDefault();

    let email = document.getElementById("party-email");
    let timeInfo = document.getElementById("party-date");
    console.log(email + " " + timeInfo + " email and date/time info");
});

function redirectCheckout(){
    let newloc = "http://shonniestudioart.com/checkout.html";
    window.location.assign(newloc);
}

function setChoice(input){
    var selection = choices[input];
    var count = document.getElementById(counters[input]).value;
    if(count > 5){
        document.getElementById(selection + 'Error').innerHTML = "Party size cannot exceed 5.";
        return;
    } else if (count == 0) {
        document.getElementById(selection + 'Error').innerHTML = "Select a party size.";
        return;
    }
    console.log(selection + " " + count)
    $.ajax({ 
        url: '/selector-process', 
        type: 'POST', 
        contentType: 'application/json', 
        data: JSON.stringify({ 
            'selection': selection, 
            'count': count,
         }), 

        error: function(error) { 
            console.log(error); 
        } 
    });
    redirectCheckout();
}