// This is your test publishable API key.
const stripe = Stripe("pk_test_51P6ith06ewSGohXen2MONsiYc8pFVY8jRMSIsJVX6ad2xqa8enBSLwHB2hlRKG9wLhX0t8P1YwPYb5ZtIuJ3G43A00Mw1YHVPU");

// The items the customer wants to buy
const items = [{ id: "xl-tshirt", id: "s-tshirt" }];

let elements;

initialize();
checkStatus();

document
  .querySelector("#payment-form")
  .addEventListener("submit", handleSubmit);

// Fetches a payment intent and captures the client secret
async function initialize() {
    const response = await fetch("/create-payment-intent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ items }),
    });
    const { clientSecret } = await response.json();

    const appearance = {
        theme: 'flat',
    };
    elements = stripe.elements({ appearance, clientSecret });

    const paymentElementOptions = {
        layout:{
            type: 'tabs',
            defaultCollapsed: false,
        },
    };

    const paymentElement = elements.create("payment", paymentElementOptions);
    paymentElement.mount("#payment-element");

    // Create and mount the Address Element in shipping mode
    const addressElement = elements.create("address", {
        mode: "billing",
        });
        
        addressElement.mount("#address-element");

        addressElement.on('change', (event) => {
        if (event.complete){
            // Extract potentially complete address
            const address = event.value.address;
        }
        })
}

async function handleSubmit(e) {
  e.preventDefault();
  setLoading(true);

  let partyName = document.getElementById("party-name");
  let email = document.getElementById("party-email");
  let dateTime = document.getElementById("party-date");

  sendData(partyName, email, dateTime);

  const { error } = await stripe.confirmPayment({
    elements,
    confirmParams: {
      // Make sure to change this to your payment completion page
      return_url: "http://shonniestudioart.com/success.html",
    },
  });

  // This point will only be reached if there is an immediate error when
  // confirming the payment. Otherwise, your customer will be redirected to
  // your `return_url`. For some payment methods like iDEAL, your customer will
  // be redirected to an intermediate site first to authorize the payment, then
  // redirected to the `return_url`.
  if (error.type === "card_error" || error.type === "validation_error") {
    showMessage(error.message);
  } else {
    showMessage("An unexpected error occurred.");
  }

  setLoading(false);
}

// Fetches the payment intent status after payment submission
async function checkStatus() {
  const clientSecret = new URLSearchParams(window.location.search).get(
    "payment_intent_client_secret"
  );

  if (!clientSecret) {
    return;
  }

  const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);

  switch (paymentIntent.status) {
    case "succeeded":
      showMessage("Payment succeeded!");
      break;
    case "processing":
      showMessage("Your payment is processing.");
      break;
    case "requires_payment_method":
      showMessage("Your payment was not successful, please try again.");
      break;
    default:
      showMessage("Something went wrong.");
      break;
  }

  sendData(email, dateTime);
}

// ------- UI helpers -------

function showMessage(messageText) {
  const messageContainer = document.querySelector("#payment-message");

  messageContainer.classList.remove("hidden");
  messageContainer.textContent = messageText;

  setTimeout(function () {
    messageContainer.classList.add("hidden");
    messageContainer.textContent = "";
  }, 4000);
}

// Show a spinner on payment submission
function setLoading(isLoading) {
  if (isLoading) {
    // Disable the button and show a spinner
    document.querySelector("#submit").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("#submit").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
}

//handles sending information to app.py
function sendData(partyName, email, dateTime){

  $.ajax({ 
      url: '/checkout-process', 
      type: 'POST', 
      contentType: 'application/json', 
      data: JSON.stringify({ 
          'email': email.value, 
          'dateTime': dateTime.value,
          'partyName': partyName.value,
       }), 

      error: function(error) { 
          console.log(error); 
      } 
  });
}