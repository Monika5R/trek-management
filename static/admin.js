/* =====================================================
   TREKORA ADMIN DASHBOARD JAVASCRIPT
   ===================================================== */


/* =====================================================
   BOOKING SEARCH + FILTER
   ===================================================== */

let currentBookingStatus = "all";


function applyBookingFilters() {

    const input =
        document.getElementById("bookingSearch");

    const searchText =
        input
        ? input.value.toLowerCase().trim()
        : "";


    const table =
        document.getElementById("bookingTable");

    if (!table) return;


    const tbody =
        table.querySelector("tbody");

    if (!tbody) return;


    const rows =
        tbody.querySelectorAll("tr");


    rows.forEach(function(row) {

        if (row.querySelector(".empty-state")) {
            return;
        }


        if (row.classList.contains("no-results-row")) {
            return;
        }


        const rowText =
            row.textContent.toLowerCase();


        const matchesSearch =
            searchText === "" ||
            rowText.includes(searchText);


        let matchesStatus = true;


        if (currentBookingStatus !== "all") {

            const statusElement =
                row.querySelector(".status");


            if (statusElement) {

                const rowStatus =
                    statusElement.textContent
                    .trim()
                    .toLowerCase();


                matchesStatus =
                    rowStatus ===
                    currentBookingStatus.toLowerCase();

            } else {

                matchesStatus = false;

            }

        }


        row.style.display =
            matchesSearch && matchesStatus
            ? ""
            : "none";

    });


    showNoResultsMessage();

}



function searchBookings() {

    applyBookingFilters();

}



function filterBookings(status, button) {

    currentBookingStatus = status;


    document
        .querySelectorAll(".filter-btn")
        .forEach(function(btn) {

            btn.classList.remove("active");

        });


    if (button) {

        button.classList.add("active");

    }


    applyBookingFilters();

}



function showNoResultsMessage() {

    const table =
        document.getElementById("bookingTable");

    if (!table) return;


    const tbody =
        table.querySelector("tbody");

    if (!tbody) return;


    const oldMessage =
        tbody.querySelector(".no-results-row");


    if (oldMessage) {

        oldMessage.remove();

    }


    const bookingRows =
        Array.from(
            tbody.querySelectorAll("tr")
        ).filter(function(row) {

            return !row.querySelector(".empty-state") &&
                   !row.classList.contains("no-results-row");

        });


    const visibleRows =
        bookingRows.filter(function(row) {

            return row.style.display !== "none";

        });


    if (
        bookingRows.length > 0 &&
        visibleRows.length === 0
    ) {

        const row =
            document.createElement("tr");


        row.className =
            "no-results-row";


        row.innerHTML = `

            <td colspan="8">

                <div class="empty-state">

                    <div class="empty-icon">

                        <svg viewBox="0 0 24 24"
                             fill="none"
                             stroke="currentColor"
                             stroke-width="1.7">

                            <circle cx="11"
                                    cy="11"
                                    r="7"/>

                            <path d="M20 20l-4-4"/>

                        </svg>

                    </div>

                    <h3>
                        No bookings found
                    </h3>

                    <p>
                        Try changing your search or status filter.
                    </p>

                </div>

            </td>

        `;


        tbody.appendChild(row);

    }

}



/* =====================================================
   MOBILE SIDEBAR
   ===================================================== */

function toggleSidebar() {

    const sidebar =
        document.querySelector(".sidebar");


    if (sidebar) {

        sidebar.classList.toggle("open");

    }

}



/* =====================================================
   TREK SEARCH + FILTER
   ===================================================== */

let currentTrekDifficulty = "all";



function searchTreks() {

    applyTrekFilters();

}



function applyTrekFilters() {

    const searchInput =
        document.getElementById("trekSearch");


    const searchText =
        searchInput
        ? searchInput.value.toLowerCase().trim()
        : "";


    const table =
        document.querySelector(".treks-table");

    if (!table) return;


    const tbody =
        table.querySelector("tbody");

    if (!tbody) return;


    const rows =
        tbody.querySelectorAll("tr");


    let visibleCount = 0;


    rows.forEach(function(row) {

        if (
            row.classList.contains("trek-no-results")
        ) {

            return;

        }


        const rowText =
            row.textContent.toLowerCase();


        const matchesSearch =
            searchText === "" ||
            rowText.includes(searchText);


        let matchesDifficulty = true;


        if (currentTrekDifficulty !== "all") {

            const difficultyElement =
                row.querySelector(".difficulty");


            if (difficultyElement) {

                const rowDifficulty =
                    difficultyElement.textContent
                    .trim()
                    .toLowerCase();


                matchesDifficulty =
                    rowDifficulty ===
                    currentTrekDifficulty.toLowerCase();

            } else {

                matchesDifficulty = false;

            }

        }


        if (
            matchesSearch &&
            matchesDifficulty
        ) {

            row.style.display = "";

            visibleCount++;

        } else {

            row.style.display = "none";

        }

    });


    showTrekNoResults(visibleCount);

}



function filterTreks(difficulty, button) {

    currentTrekDifficulty =
        difficulty;


    document
        .querySelectorAll(".trek-filter-btn")
        .forEach(function(btn) {

            btn.classList.remove("active");

        });


    if (button) {

        button.classList.add("active");

    }


    applyTrekFilters();

}



function showTrekNoResults(visibleCount) {

    const tbody =
        document.querySelector(
            ".treks-table tbody"
        );


    if (!tbody) return;


    const oldMessage =
        tbody.querySelector(
            ".trek-no-results"
        );


    if (oldMessage) {

        oldMessage.remove();

    }


    if (visibleCount > 0) {

        return;

    }


    const row =
        document.createElement("tr");


    row.className =
        "trek-no-results";


    row.innerHTML = `

        <td colspan="8">

            <div class="trek-empty-state">

                <div class="trek-empty-icon">

                    <svg viewBox="0 0 24 24"
                         fill="none"
                         stroke="currentColor"
                         stroke-width="2">

                        <circle cx="11"
                                cy="11"
                                r="7"/>

                        <path d="M20 20l-4-4"/>

                    </svg>

                </div>

                <h3>
                    No treks found
                </h3>

                <p>
                    Try a different search or difficulty.
                </p>

            </div>

        </td>

    `;


    tbody.appendChild(row);

}



/* =====================================================
   ADD TREK MODAL
   ===================================================== */

function openAddTrekModal() {

    const modal =
        document.getElementById("addTrekModal");


    if (modal) {

        modal.classList.add("show");

    }

}



function closeAddTrekModal() {

    const modal =
        document.getElementById("addTrekModal");


    if (modal) {

        modal.classList.remove("show");

    }

}



/* =====================================================
   IMAGE PREVIEW
   ===================================================== */

function setupTrekImagePreview() {

    const trekImageInput =
        document.getElementById("trekImage");


    const trekImagePreview =
        document.getElementById(
            "trekImagePreview"
        );


    if (
        !trekImageInput ||
        !trekImagePreview
    ) {

        return;

    }


    trekImageInput.addEventListener(
        "change",
        function() {

            const file =
                this.files[0];


            if (!file) {

                trekImagePreview.innerHTML = "";

                trekImagePreview.classList.remove(
                    "show"
                );

                return;

            }


            if (
                !file.type.startsWith("image/")
            ) {

                alert(
                    "Please select a valid image file."
                );

                this.value = "";

                trekImagePreview.innerHTML = "";

                trekImagePreview.classList.remove(
                    "show"
                );

                return;

            }


            const reader =
                new FileReader();


            reader.onload =
                function(event) {

                    trekImagePreview.innerHTML = `

                        <div class="preview-container">

                            <img
                                src="${event.target.result}"
                                alt="Trek Image Preview">

                            <div class="preview-info">

                                <strong>
                                    ${file.name}
                                </strong>

                                <span>
                                    ${(file.size / 1024).toFixed(1)} KB
                                </span>

                            </div>

                        </div>

                    `;


                    trekImagePreview.classList.add(
                        "show"
                    );

                };


            reader.readAsDataURL(file);

        }
    );

}



/* =====================================================
   USERS SEARCH
   ===================================================== */

function searchUsers() {

    const input =
        document.getElementById("userSearch");


    const table =
        document.getElementById("usersTable");


    if (!input || !table) {

        return;

    }


    const searchText =
        input.value
        .toLowerCase()
        .trim();


    const rows =
        table.querySelectorAll("tbody tr");


    rows.forEach(function(row) {

        const rowText =
            row.textContent.toLowerCase();


        if (rowText.includes(searchText)) {

            row.style.display = "";

        } else {

            row.style.display = "none";

        }

    });

}



/* =====================================================
   PAGE LOAD
   ===================================================== */

document.addEventListener(
    "DOMContentLoaded",
    function() {


        /* ---------------------------------------------
           ADD TREK BUTTON
           --------------------------------------------- */

        const addTrekButton =
            document.querySelector(
                ".add-trek-btn"
            );


        if (addTrekButton) {

            addTrekButton.addEventListener(
                "click",
                openAddTrekModal
            );

        }



        /* ---------------------------------------------
           TREK SEARCH
           --------------------------------------------- */

        const trekSearchInput =
            document.getElementById(
                "trekSearch"
            );


        if (trekSearchInput) {

            trekSearchInput.addEventListener(
                "input",
                searchTreks
            );

        }



        /* ---------------------------------------------
           TREK DIFFICULTY FILTERS
           --------------------------------------------- */

        document
            .querySelectorAll(
                ".trek-filter-btn"
            )
            .forEach(function(button) {

                button.addEventListener(
                    "click",
                    function() {

                        const difficulty =
                            this.getAttribute(
                                "data-difficulty"
                            );


                        filterTreks(
                            difficulty,
                            this
                        );

                    }
                );

            });



        /* ---------------------------------------------
           TREK IMAGE PREVIEW
           --------------------------------------------- */

        setupTrekImagePreview();

    }
);

/* =====================================================
   PAYMENT SEARCH + FILTER
   ===================================================== */

let currentPaymentStatus = "all";


function searchPayments() {

    applyPaymentFilters();

}


function filterPayments(status, button) {

    currentPaymentStatus = status;


    document
        .querySelectorAll(".payment-filter-btn")
        .forEach(function(btn) {

            btn.classList.remove("active");

        });


    if (button) {

        button.classList.add("active");

    }


    applyPaymentFilters();

}


function applyPaymentFilters() {

    const input =
        document.getElementById("paymentSearch");


    const table =
        document.getElementById("paymentsTable");


    if (!input || !table) {

        return;

    }


    const searchText =
        input.value
        .toLowerCase()
        .trim();


    const rows =
        table.querySelectorAll(
            "tbody tr"
        );


    let visibleCount = 0;


    rows.forEach(function(row) {

        /*
         * Ignore empty-state rows
         */
        if (
            row.querySelector(
                ".payment-empty-state"
            )
        ) {

            return;

        }


        /*
         * Ignore no-result row
         */
        if (
            row.classList.contains(
                "payment-no-results"
            )
        ) {

            return;

        }


        const rowText =
            row.textContent
            .toLowerCase();


        /*
         * Search
         */
        const matchesSearch =
            searchText === "" ||
            rowText.includes(searchText);


        /*
         * Payment status
         */
        let matchesStatus = true;


        if (
            currentPaymentStatus !== "all"
        ) {

            const statusElement =
                row.querySelector(
                    ".payment-status"
                );


            if (statusElement) {

                const rowStatus =
                    statusElement.textContent
                    .trim()
                    .toLowerCase();


                matchesStatus =
                    rowStatus ===
                    currentPaymentStatus
                    .toLowerCase();

            } else {

                matchesStatus = false;

            }

        }


        /*
         * Show / hide row
         */
        if (
            matchesSearch &&
            matchesStatus
        ) {

            row.style.display = "";

            visibleCount++;

        } else {

            row.style.display = "none";

        }

    });


    showPaymentNoResults(
        visibleCount
    );

}


function showPaymentNoResults(
    visibleCount
) {

    const table =
        document.getElementById(
            "paymentsTable"
        );


    if (!table) {

        return;

    }


    const tbody =
        table.querySelector("tbody");


    if (!tbody) {

        return;

    }


    /*
     * Remove old no-result message
     */
    const oldMessage =
        tbody.querySelector(
            ".payment-no-results"
        );


    if (oldMessage) {

        oldMessage.remove();

    }


    /*
     * Check actual payment rows
     */
    const paymentRows =
        Array.from(
            tbody.querySelectorAll("tr")
        ).filter(function(row) {

            return !row.querySelector(
                ".payment-empty-state"
            ) &&
            !row.classList.contains(
                "payment-no-results"
            );

        });


    /*
     * If there are payment records
     * but none match the search/filter
     */
    if (
        paymentRows.length > 0 &&
        visibleCount === 0
    ) {

        const row =
            document.createElement("tr");


        row.className =
            "payment-no-results";


        row.innerHTML = `

            <td colspan="8">

                <div class="payment-empty-state">

                    <div class="payment-empty-icon">

                        <svg
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="1.8">

                            <circle
                                cx="11"
                                cy="11"
                                r="7"/>

                            <path
                                d="m20 20-4-4"/>

                        </svg>

                    </div>


                    <h3>
                        No payments found
                    </h3>


                    <p>
                        Try changing your search
                        or payment status filter.
                    </p>

                </div>

            </td>

        `;


        tbody.appendChild(row);

    }

}

function searchMentors() {

    const input =
        document.getElementById("mentorSearch");

    const table =
        document.getElementById("mentorsTable");

    if (!input || !table) {
        return;
    }

    const searchText =
        input.value.toLowerCase().trim();

    const rows =
        table.querySelectorAll("tbody tr");

    rows.forEach(function(row) {

        if (
            row.querySelector(".mentors-empty-state")
        ) {
            return;
        }

        const rowText =
            row.textContent.toLowerCase();

        if (
            searchText === "" ||
            rowText.includes(searchText)
        ) {

            row.style.display = "";

        } else {

            row.style.display = "none";

        }

    });

}


// =========================================================
// PAYMENTS MANAGEMENT
// =========================================================


// =========================================================
// SEARCH PAYMENTS
// =========================================================

function searchPayments() {

    const searchInput =
        document.getElementById("paymentSearch");

    const table =
        document.getElementById("paymentsTable");

    if (!searchInput || !table) {

        return;

    }

    const searchValue =
        searchInput.value
            .toLowerCase()
            .trim();

    const rows =
        table.querySelectorAll(
            "tbody tr"
        );

    rows.forEach(function(row) {

        const rowText =
            row.textContent
                .toLowerCase();

        if (
            rowText.includes(
                searchValue
            )
        ) {

            row.style.display = "";

        } else {

            row.style.display = "none";

        }

    });

}


// =========================================================
// FILTER PAYMENTS
// =========================================================

function filterPayments(
    status,
    button
) {

    const table =
        document.getElementById(
            "paymentsTable"
        );

    if (!table) {

        return;

    }


    // =====================================================
    // UPDATE ACTIVE FILTER BUTTON
    // =====================================================

    const filterButtons =
        document.querySelectorAll(
            ".payment-filter-btn"
        );

    filterButtons.forEach(
        function(filterButton) {

            filterButton.classList.remove(
                "active"
            );

        }
    );


    if (button) {

        button.classList.add(
            "active"
        );

    }


    // =====================================================
    // FILTER TABLE ROWS
    // =====================================================

    const rows =
        table.querySelectorAll(
            "tbody tr"
        );

    rows.forEach(function(row) {

        const paymentStatusElement =
            row.querySelector(
                ".payment-status"
            );


        // Empty state row

        if (!paymentStatusElement) {

            return;

        }


        const paymentStatus =
            paymentStatusElement.textContent
                .toLowerCase()
                .trim();


        // =================================================
        // SHOW ALL
        // =================================================

        if (status === "all") {

            row.style.display = "";

            return;

        }


        // =================================================
        // SHOW MATCHING STATUS
        // =================================================

        if (
            paymentStatus ===
            status.toLowerCase()
        ) {

            row.style.display = "";

        } else {

            row.style.display = "none";

        }

    });

}

// =========================================================
// ADMIN PROFILE SETTINGS
// =========================================================

function saveAdminProfile() {

    const adminName =
        document.getElementById("adminName");

    const adminEmail =
        document.getElementById("adminEmail");

    if (!adminName || !adminEmail) {
        return;
    }

    const name =
        adminName.value.trim();

    const email =
        adminEmail.value.trim();

    if (name === "") {
        alert("Please enter the admin name.");
        adminName.focus();
        return;
    }

    if (email === "") {
        alert("Please enter the admin email.");
        adminEmail.focus();
        return;
    }

    localStorage.setItem(
        "trekoraAdminName",
        name
    );

    localStorage.setItem(
        "trekoraAdminEmail",
        email
    );

    alert("Admin profile saved successfully.");
}

// =========================================================
// WEBSITE SETTINGS
// =========================================================

function saveWebsiteSettings() {

    const websiteName =
        document.getElementById("websiteName");

    const contactEmail =
        document.getElementById("contactEmail");

    const contactPhone =
        document.getElementById("contactPhone");

    const websiteLocation =
        document.getElementById("websiteLocation");

    if (
        !websiteName ||
        !contactEmail ||
        !contactPhone ||
        !websiteLocation
    ) {
        return;
    }

    const name =
        websiteName.value.trim();

    const email =
        contactEmail.value.trim();

    const phone =
        contactPhone.value.trim();

    const location =
        websiteLocation.value.trim();


    if (name === "") {

        alert("Please enter the website name.");

        websiteName.focus();

        return;
    }


    if (email === "") {

        alert("Please enter the contact email.");

        contactEmail.focus();

        return;
    }


    if (phone === "") {

        alert("Please enter the contact phone.");

        contactPhone.focus();

        return;
    }


    if (location === "") {

        alert("Please enter the website location.");

        websiteLocation.focus();

        return;
    }


    localStorage.setItem(
        "trekoraWebsiteName",
        name
    );

    localStorage.setItem(
        "trekoraContactEmail",
        email
    );

    localStorage.setItem(
        "trekoraContactPhone",
        phone
    );

    localStorage.setItem(
        "trekoraWebsiteLocation",
        location
    );


    alert("Website settings saved successfully.");
}

// =========================================================
// BOOKING SETTINGS
// =========================================================

function saveBookingSettings() {

    const allowBookings =
        document.getElementById("allowBookings");

    const autoConfirmation =
        document.getElementById("autoConfirmation");

    const maxTravellers =
        document.getElementById("maxTravellers");

    if (
        !allowBookings ||
        !autoConfirmation ||
        !maxTravellers
    ) {
        return;
    }

    const bookingsAllowed =
        allowBookings.checked;

    const automaticConfirmation =
        autoConfirmation.checked;

    const maximumTravellers =
        parseInt(
            maxTravellers.value,
            10
        );

    if (
        isNaN(maximumTravellers) ||
        maximumTravellers < 1 ||
        maximumTravellers > 50
    ) {

        alert(
            "Maximum travellers must be between 1 and 50."
        );

        maxTravellers.focus();

        return;
    }

    const settings = [
        {
            setting_name: "allow_bookings",
            setting_value: bookingsAllowed
        },
        {
            setting_name: "auto_confirmation",
            setting_value: automaticConfirmation
        },
        {
            setting_name: "max_travellers",
            setting_value: maximumTravellers
        }
    ];

    Promise.all(
        settings.map(function(setting) {

            return fetch(
                "/admin/update-booking-setting",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(setting)
                }
            )
            .then(function(response) {
                return response.json();
            });
        })
    )
    .then(function(results) {

        const failed =
            results.some(function(result) {
                return !result.success;
            });

        if (failed) {

            alert(
                "Some booking settings could not be saved."
            );

            return;
        }

        alert(
            "Booking settings saved successfully."
        );

    })
    .catch(function(error) {

        console.error(
            "Booking Settings Error:",
            error
        );

        alert(
            "Unable to save booking settings."
        );
    });
}
// =========================================================
// NOTIFICATION SETTINGS
// =========================================================

function saveNotificationSettings() {

    const bookingNotifications =
        document.getElementById("bookingNotifications");

    const paymentNotifications =
        document.getElementById("paymentNotifications");

    const cancellationNotifications =
        document.getElementById("cancellationNotifications");


    if (
        !bookingNotifications ||
        !paymentNotifications ||
        !cancellationNotifications
    ) {
        return;
    }


    const newBookingNotifications =
        bookingNotifications.checked;

    const paymentStatusNotifications =
        paymentNotifications.checked;

    const cancellationNotificationsEnabled =
        cancellationNotifications.checked;


    localStorage.setItem(
        "trekoraBookingNotifications",
        newBookingNotifications
    );

    localStorage.setItem(
        "trekoraPaymentNotifications",
        paymentStatusNotifications
    );

    localStorage.setItem(
        "trekoraCancellationNotifications",
        cancellationNotificationsEnabled
    );


    alert(
        "Notification settings saved successfully."
    );
}

function saveNotificationSetting(
    settingName,
    settingValue
) {

    fetch(
        "/admin/update-notification-setting",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                setting_name: settingName,
                setting_value: settingValue
            })
        }
    )
    .then(function(response) {
        return response.json();
    })
    .then(function(result) {

        if (!result.success) {

            alert(
                result.message ||
                "Unable to update notification setting."
            );

            return;
        }

        console.log(
            "Notification setting updated:",
            settingName,
            "=",
            settingValue
        );

    })
    .catch(function(error) {

        console.error(
            "Notification Setting Error:",
            error
        );

        alert(
            "Unable to update notification setting."
        );

    });
}

function updateNotificationBadge() {

    const badge =
        document.getElementById(
            "notificationBadge"
        );

    if (!badge) {
        return;
    }


    fetch("/admin/notifications")
        .then(function(response) {

            return response.json();

        })
        .then(function(data) {

            if (!data.success) {
                return;
            }


            const unreadCount =
                data.unread_count;


            if (unreadCount > 0) {

                badge.textContent =
                    unreadCount;

                badge.style.display =
                    "flex";

            } else {

                badge.textContent =
                    "0";

                badge.style.display =
                    "none";
            }

        })
        .catch(function(error) {

            console.error(
                "Notification Error:",
                error
            );

        });
}

document.addEventListener(
    "DOMContentLoaded",
    function() {

        updateNotificationBadge();

    }
);

function toggleNotifications() {

    const panel =
        document.getElementById(
            "notificationPanel"
        );

    if (!panel) {
        return;
    }


    const isOpen =
        panel.classList.contains(
            "show"
        );


    if (isOpen) {

        panel.classList.remove(
            "show"
        );

        return;
    }


    panel.classList.add(
        "show"
    );


    loadAdminNotifications();
}

function loadAdminNotifications() {

    const list =
        document.getElementById(
            "notificationList"
        );

    if (!list) {
        return;
    }


    list.innerHTML = `
        <div class="notification-loading">
            Loading notifications...
        </div>
    `;


    fetch(
        "/admin/notifications/list"
    )
        .then(function(response) {

            return response.json();

        })
        .then(function(data) {

            if (!data.success) {

                list.innerHTML = `
                    <div class="notification-empty">
                        Unable to load notifications.
                    </div>
                `;

                return;
            }


            if (
                !data.notifications ||
                data.notifications.length === 0
            ) {

                list.innerHTML = `
                    <div class="notification-empty">
                        <strong>No notifications</strong>
                        <span>
                            You're all caught up.
                        </span>
                    </div>
                `;

                return;
            }


            list.innerHTML = "";


            data.notifications.forEach(
                function(notification) {

                    const item =
                        document.createElement(
                            "div"
                        );

                    item.className =
                        "notification-item";


                    if (
                        !notification.is_read
                    ) {

                        item.classList.add(
                            "unread"
                        );

                    }


                    item.innerHTML = `
                        <div class="notification-item-icon">
                            ${getNotificationIcon(
                                notification.type
                            )}
                        </div>

                        <div class="notification-item-content">

                            <strong>
                                ${escapeNotificationText(
                                    notification.title
                                )}
                            </strong>

                            <p>
                                ${escapeNotificationText(
                                    notification.message
                                )}
                            </p>

                            ${
                                notification.booking_id
                                ? `
                                    <span class="notification-booking">
                                        Booking:
                                        ${escapeNotificationText(
                                            notification.booking_id
                                        )}
                                    </span>
                                `
                                : ""
                            }

                            <small>
                                ${formatNotificationTime(
                                    notification.created_at
                                )}
                            </small>

                        </div>
                    `;


                    list.appendChild(
                        item
                    );

                }
            );

        })
        .catch(function(error) {

            console.error(
                "Notification Load Error:",
                error
            );


            list.innerHTML = `
                <div class="notification-empty">
                    Unable to load notifications.
                </div>
            `;

        });
}

function getNotificationIcon(
    notificationType
) {

    if (
        notificationType ===
        "booking"
    ) {

        return "📅";

    }


    if (
        notificationType ===
        "payment"
    ) {

        return "💳";

    }


    if (
        notificationType ===
        "cancellation"
    ) {

        return "⚠";

    }


    return "🔔";
}
function escapeNotificationText(
    text
) {

    if (!text) {
        return "";
    }


    const element =
        document.createElement(
            "div"
        );

    element.textContent =
        text;


    return element.innerHTML;
}
function formatNotificationTime(
    createdAt
) {

    if (!createdAt) {
        return "";
    }


    const date =
        new Date(
            createdAt
        );


    if (
        Number.isNaN(
            date.getTime()
        )
    ) {

        return "";
    }


    return date.toLocaleString(
        "en-IN",
        {
            day: "2-digit",
            month: "short",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit"
        }
    );
}