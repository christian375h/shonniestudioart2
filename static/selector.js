const counters = [
  "facePaintCounter",
  "glitterTattoosCounter",
  "paintNightCounter",
];

const choices = ["facePaint", "glitterTattoos", "paintNight"];

function setFace() {
  setChoice(0);
}
function setTattoo() {
  setChoice(1);
}
function setNight() {
  setChoice(2);
}

let dateTime = document.getElementById("contact-info-form");
dateTime.addEventListener("submit", (e) => {
  e.preventDefault();

  let email = document.getElementById("party-email");
  let timeInfo = document.getElementById("party-date");
  console.log(email + " " + timeInfo + " email and date/time info");
});

function redirectCheckout() {
  let newloc = "http://shonniestudioart.com/checkout.html";
  window.location.assign(newloc);
}

function setChoice(input) {
  var selection = choices[input];
  var partySize = document.getElementById(counters[input]).value;
  var maxSize = 0;
  var partyMultiple = 0;

  if (selection == "facePaint" || selection == "glitterTattoos") {
    maxSize = 500;
    partyMultiple = 20;
  } else {
    partyMultiple = 1;
    maxSize = 50;
  }

  if (partySize > maxSize) {
    document.getElementById(selection + "Error").innerHTML =
      "Party size cannot exceed " + maxSize + ".";
    return;
  } else if (partySize == 0) {
    document.getElementById(selection + "Error").innerHTML =
      "Select a party size.";
    return;
  } else if (partySize % partyMultiple != 0) {
    document.getElementById(selection + "Error").innerHTML =
      "Max party size must be a multiple of " + partyMultiple + ".";
    return;
  }

  console.log(selection + " " + partySize + " ");
  $.ajax({
    url: "/selector-process",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({
      selection: selection,
      count: partySize / partyMultiple,
      partySize: partySize,
    }),

    error: function (error) {
      console.log(error);
    },
  });
  redirectCheckout();
}
