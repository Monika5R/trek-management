// ================= BOOK TREK =================

function bookTrek(trekName) {

    alert(
        "You selected " +
        trekName +
        ". Booking feature will be added soon!"
    );

}


// ================= AI TREK FINDER =================

function showAIMessage() {

    alert(
        "🤖 AI Recommendation\n\n" +
        "This feature will recommend the best trek " +
        "based on your preferences."
    );

}


// ================= VIEW TREK =================

function viewTrek(trekName) {

    alert(
        "Opening details for " +
        trekName
    );

}


// ================= SIMPLE TREK SEARCH =================

function searchTrekByName() {

    const searchInput =
        document.getElementById("trekSearchInput");

    if (!searchInput) {
        return;
    }


    const searchText =
        searchInput.value.trim().toLowerCase();


    if (searchText === "") {

        alert("Please enter a trek name.");

        searchInput.focus();

        return;
    }


    const trekCards =
        document.querySelectorAll(".trek-card");


    let foundTrek = null;


    trekCards.forEach(function(card) {

        const trekNameElement =
            card.querySelector("h3");


        if (!trekNameElement) {
            return;
        }


        const trekName =
            trekNameElement.textContent
                .trim()
                .toLowerCase();


        if (trekName.includes(searchText)) {

            foundTrek = trekNameElement
                .textContent
                .trim();

        }

    });


    if (foundTrek) {

        /*
         * Open the trek details page.
         *
         * encodeURIComponent makes names
         * containing spaces safe in the URL.
         */

        window.location.href =
            "/trek/" +
            encodeURIComponent(foundTrek);

        return;
    }


    alert(
        "No trek found for \"" +
        searchInput.value.trim() +
        "\"."
    );

}


// ================= ENTER KEY SEARCH =================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        const searchInput =
            document.getElementById("trekSearchInput");


        if (!searchInput) {
            return;
        }


        searchInput.addEventListener(
            "keydown",
            function(event) {

                if (event.key === "Enter") {

                    event.preventDefault();

                    searchTrekByName();

                }

            }
        );

    }
);