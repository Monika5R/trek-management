/* =========================================================
   TREKORA BOOKING PAGE
   booking.js
   ========================================================= */


/* =========================================================
   TREK PRICE
   ========================================================= */
/* =========================================================
   TREK PRICE
   ========================================================= */

const bookingData =
    document.getElementById("booking-data");

const trekPrice =
    bookingData
        ? Number(
            JSON.parse(
                bookingData.textContent
            ).trekPrice
        )
        : 0;


/* =========================================================
   GET ELEMENTS
   ========================================================= */

const bookingForm =
    document.getElementById("bookingForm");

const peopleInput =
    document.getElementById("people");

const trekDateInput =
    document.getElementById("trek_date");

const submitButton =
    document.getElementById("submitBookingBtn");


/* =========================================================
   PAYMENT PANELS
   ========================================================= */

const upiPanel =
    document.getElementById("upiPanel");

const cardPanel =
    document.getElementById("cardPanel");

const bankPanel =
    document.getElementById("bankPanel");

const cashPanel =
    document.getElementById("cashPanel");


/* =========================================================
   PAYMENT INPUTS
   ========================================================= */

const upiInput =
    document.getElementById("upi_id");

const cardNumberInput =
    document.getElementById("card_number");

const cardExpiryInput =
    document.getElementById("card_expiry");

const cardCVVInput =
    document.getElementById("card_cvv");

const cardNameInput =
    document.getElementById("card_name");

const bankInput =
    document.getElementById("bank_name");


/* =========================================================
   PRICE ELEMENTS
   ========================================================= */

const personCount =
    document.getElementById("personCount");

const totalAmount =
    document.getElementById("totalAmount");

const upiAmount =
    document.getElementById("upiAmount");

const cardAmount =
    document.getElementById("cardAmount");

const bankAmount =
    document.getElementById("bankAmount");

const cashAmount =
    document.getElementById("cashAmount");


/* =========================================================
   FORMAT CURRENCY
   ========================================================= */

function formatCurrency(amount) {

    return "₹" +
        Number(amount).toLocaleString("en-IN");

}


/* =========================================================
   CALCULATE TOTAL
   ========================================================= */

function calculateTotal() {

    if (!peopleInput) {
        return;
    }

    const people =
        parseInt(peopleInput.value) || 1;


    const total =
        trekPrice * people;


    if (personCount) {

        personCount.innerText =
            people;

    }


    if (totalAmount) {

        totalAmount.innerText =
            formatCurrency(total);

    }


    if (upiAmount) {

        upiAmount.innerText =
            formatCurrency(total);

    }


    if (cardAmount) {

        cardAmount.innerText =
            formatCurrency(total);

    }


    if (bankAmount) {

        bankAmount.innerText =
            formatCurrency(total);

    }


    if (cashAmount) {

        cashAmount.innerText =
            formatCurrency(total);

    }

}


/* =========================================================
   PAYMENT METHOD
   ========================================================= */

function getSelectedPaymentMethod() {

    const selected =
        document.querySelector(
            'input[name="payment_method"]:checked'
        );

    if (!selected) {
        return "";
    }

    return selected.value;

}


/* =========================================================
   HIDE ALL PAYMENT PANELS
   ========================================================= */

function hidePaymentPanels() {

    if (upiPanel) {
        upiPanel.classList.remove("show");
    }

    if (cardPanel) {
        cardPanel.classList.remove("show");
    }

    if (bankPanel) {
        bankPanel.classList.remove("show");
    }

    if (cashPanel) {
        cashPanel.classList.remove("show");
    }

}


/* =========================================================
   ENABLE / DISABLE PAYMENT INPUTS
   ========================================================= */

function setPaymentInputs() {

    const method =
        getSelectedPaymentMethod();


    /*
       Disable all optional payment inputs first.
    */

    if (upiInput) {
        upiInput.disabled = true;
        upiInput.required = false;
    }


    if (cardNumberInput) {
        cardNumberInput.disabled = true;
        cardNumberInput.required = false;
    }


    if (cardExpiryInput) {
        cardExpiryInput.disabled = true;
        cardExpiryInput.required = false;
    }


    if (cardCVVInput) {
        cardCVVInput.disabled = true;
        cardCVVInput.required = false;
    }


    if (cardNameInput) {
        cardNameInput.disabled = true;
        cardNameInput.required = false;
    }


    if (bankInput) {
        bankInput.disabled = true;
        bankInput.required = false;
    }


    /*
       Enable fields according to
       selected payment method.
    */

    if (method === "UPI") {

        if (upiInput) {

            upiInput.disabled = false;
            upiInput.required = true;

        }

    }


    if (
        method === "Credit Card" ||
        method === "Debit Card"
    ) {

        if (cardNumberInput) {

            cardNumberInput.disabled = false;
            cardNumberInput.required = true;

        }


        if (cardExpiryInput) {

            cardExpiryInput.disabled = false;
            cardExpiryInput.required = true;

        }


        if (cardCVVInput) {

            cardCVVInput.disabled = false;
            cardCVVInput.required = true;

        }


        if (cardNameInput) {

            cardNameInput.disabled = false;
            cardNameInput.required = true;

        }

    }


    if (method === "Net Banking") {

        if (bankInput) {

            bankInput.disabled = false;
            bankInput.required = true;

        }

    }

}


/* =========================================================
   SHOW SELECTED PAYMENT PANEL
   ========================================================= */

function showPaymentPanel() {

    hidePaymentPanels();

    setPaymentInputs();


    const method =
        getSelectedPaymentMethod();


    if (method === "UPI") {

        if (upiPanel) {
            upiPanel.classList.add("show");
        }

    }


    if (
        method === "Credit Card" ||
        method === "Debit Card"
    ) {

        if (cardPanel) {
            cardPanel.classList.add("show");
        }

    }


    if (method === "Net Banking") {

        if (bankPanel) {
            bankPanel.classList.add("show");
        }

    }


    if (method === "Cash") {

        if (cashPanel) {
            cashPanel.classList.add("show");
        }

    }

}


/* =========================================================
   PAYMENT RADIO BUTTONS
   ========================================================= */

const paymentMethods =
    document.querySelectorAll(
        'input[name="payment_method"]'
    );


paymentMethods.forEach(function(radio) {

    radio.addEventListener(
        "change",
        function() {

            showPaymentPanel();

        }
    );

});


/* =========================================================
   PEOPLE CHANGE
   ========================================================= */

if (peopleInput) {

    peopleInput.addEventListener(
        "change",
        function() {

            calculateTotal();

        }
    );

}


/* =========================================================
   PHONE NUMBER VALIDATION
   ========================================================= */

const phoneInput =
    document.getElementById("phone");

const emergencyPhoneInput =
    document.getElementById("emergency_phone");


function allowOnlyNumbers(input) {

    if (!input) {
        return;
    }


    input.addEventListener(
        "input",
        function() {

            this.value =
                this.value.replace(
                    /[^0-9]/g,
                    ""
                );

        }
    );

}


allowOnlyNumbers(phoneInput);

allowOnlyNumbers(emergencyPhoneInput);

allowOnlyNumbers(cardCVVInput);


/* =========================================================
   CARD NUMBER FORMATTING
   ========================================================= */

if (cardNumberInput) {

    cardNumberInput.addEventListener(
        "input",
        function() {

            let value =
                this.value.replace(
                    /\D/g,
                    ""
                );


            value =
                value.substring(0, 16);


            let formatted = "";


            for (
                let i = 0;
                i < value.length;
                i++
            ) {

                if (
                    i > 0 &&
                    i % 4 === 0
                ) {

                    formatted += " ";

                }

                formatted += value[i];

            }


            this.value = formatted;

        }
    );

}


/* =========================================================
   CARD EXPIRY FORMATTING
   ========================================================= */

if (cardExpiryInput) {

    cardExpiryInput.addEventListener(
        "input",
        function() {

            let value =
                this.value.replace(
                    /\D/g,
                    ""
                );


            value =
                value.substring(0, 4);


            if (value.length >= 3) {

                value =
                    value.substring(0, 2) +
                    " / " +
                    value.substring(2);

            }


            this.value = value;

        }
    );

}


/* =========================================================
   UPI VALIDATION
   ========================================================= */

function validateUPI() {

    if (!upiInput) {
        return true;
    }


    const value =
        upiInput.value.trim();


    if (value === "") {

        alert(
            "Please enter your UPI ID."
        );

        upiInput.focus();

        return false;

    }


    const upiPattern =
        /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+$/;


    if (!upiPattern.test(value)) {

        alert(
            "Please enter a valid UPI ID.\n\n" +
            "Example: example@upi"
        );

        upiInput.focus();

        return false;

    }


    return true;

}


/* =========================================================
   CARD VALIDATION
   ========================================================= */

function validateCard() {

    if (
        !cardNumberInput ||
        !cardExpiryInput ||
        !cardCVVInput ||
        !cardNameInput
    ) {

        return true;

    }


    const cardNumber =
        cardNumberInput.value
            .replace(/\s/g, "");


    const expiry =
        cardExpiryInput.value
            .replace(/\s/g, "");


    const cvv =
        cardCVVInput.value.trim();


    const cardName =
        cardNameInput.value.trim();


    if (cardNumber.length !== 16) {

        alert(
            "Please enter a valid 16-digit card number."
        );

        cardNumberInput.focus();

        return false;

    }


    if (!/^\d{2}\/\d{2}$/.test(expiry)) {

        alert(
            "Please enter the card expiry date in MM / YY format."
        );

        cardExpiryInput.focus();

        return false;

    }


    const parts =
        expiry.split("/");


    const month =
        parseInt(parts[0]);


    if (
        month < 1 ||
        month > 12
    ) {

        alert(
            "Please enter a valid expiry month."
        );

        cardExpiryInput.focus();

        return false;

    }


    if (cvv.length !== 3) {

        alert(
            "Please enter a valid 3-digit CVV."
        );

        cardCVVInput.focus();

        return false;

    }


    if (cardName.length < 2) {

        alert(
            "Please enter the cardholder name."
        );

        cardNameInput.focus();

        return false;

    }


    return true;

}


/* =========================================================
   NET BANKING VALIDATION
   ========================================================= */

function validateNetBanking() {

    if (!bankInput) {
        return true;
    }


    if (bankInput.value === "") {

        alert(
            "Please select your bank."
        );

        bankInput.focus();

        return false;

    }


    return true;

}


/* =========================================================
   PAYMENT VALIDATION
   ========================================================= */

function validatePayment() {

    const method =
        getSelectedPaymentMethod();


    if (!method) {

        alert(
            "Please select a payment method."
        );

        return false;

    }


    if (method === "UPI") {

        return validateUPI();

    }


    if (
        method === "Credit Card" ||
        method === "Debit Card"
    ) {

        return validateCard();

    }


    if (method === "Net Banking") {

        return validateNetBanking();

    }


    if (method === "Cash") {

        return true;

    }


    return true;

}


/* =========================================================
   DATE VALIDATION
   ========================================================= */

function setMinimumDate() {

    if (!trekDateInput) {
        return;
    }


    const today =
        new Date();


    const year =
        today.getFullYear();


    const month =
        String(
            today.getMonth() + 1
        ).padStart(2, "0");


    const day =
        String(
            today.getDate()
        ).padStart(2, "0");


    const formattedDate =
        `${year}-${month}-${day}`;


    trekDateInput.min =
        formattedDate;

}


setMinimumDate();


/* =========================================================
   BOOKING FORM SUBMISSION
   ========================================================= */

if (bookingForm) {

    bookingForm.addEventListener(
        "submit",
        function(event) {

            /*
               Browser validation first.
            */

            if (!bookingForm.checkValidity()) {

                event.preventDefault();

                bookingForm.reportValidity();

                return;

            }


            /*
               Payment validation.
            */

            if (!validatePayment()) {

                event.preventDefault();

                return;

            }


            /*
               Trek date validation.
            */

            if (
                trekDateInput &&
                trekDateInput.value === ""
            ) {

                event.preventDefault();

                alert(
                    "Please select your trek date."
                );

                trekDateInput.focus();

                return;

            }


            /*
               Prevent multiple clicks.
            */

            if (submitButton) {

                submitButton.disabled = true;

                submitButton.classList.add(
                    "loading"
                );

            }

        }
    );

}


/* =========================================================
   INITIALIZE
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function() {

        calculateTotal();

        hidePaymentPanels();

        setPaymentInputs();

    }
);