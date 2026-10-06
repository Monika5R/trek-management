from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import unquote_plus
from ai.trek_recommender import recommend_treks
from database import save_booking, get_db_connection, get_all_mentors, get_all_users,get_admin_setting,update_admin_setting,create_notification,get_notifications
import uuid
import os
from werkzeug.utils import secure_filename


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)
app.secret_key = "trekora_secret_key_2026"


# =========================================================
# UPLOAD SETTINGS
# =========================================================

UPLOAD_FOLDER = os.path.join("static", "images")

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# =========================================================
# DEFAULT TREK DATA
# =========================================================

default_treks = {

    "Kudremukh": {
        "name": "Kudremukh",
        "location": "Chikkamagaluru",
        "image": "kudremukh.png",
        "difficulty": "Moderate",
        "duration": "2 Days",
        "distance": "22 km",
        "elevation": "1,894 m",
        "price": 1499,
        "rating": 4.8,
        "mentor": "Arjun Kumar",
        "short_description": "A beautiful mountain trek through lush green landscapes.",
        "description": "Kudremukh is one of Karnataka's most scenic trekking destinations, famous for rolling grasslands, misty mountains and beautiful forest trails."
    },

    "Skandagiri": {
        "name": "Skandagiri",
        "location": "Chikkaballapur",
        "image": "skandagiri.png",
        "difficulty": "Easy",
        "duration": "1 Day",
        "distance": "8 km",
        "elevation": "1,450 m",
        "price": 899,
        "rating": 4.7,
        "mentor": "Rahul Shetty",
        "short_description": "A popular sunrise trek near Bengaluru.",
        "description": "Skandagiri is a beautiful hill trek known for its sunrise views, peaceful surroundings and moderate trail."
    },

    "Kumara Parvatha": {
        "name": "Kumara Parvatha",
        "location": "Coorg",
        "image": "kumara-parvatha.png",
        "difficulty": "Difficult",
        "duration": "2 Days",
        "distance": "25 km",
        "elevation": "1,712 m",
        "price": 1799,
        "rating": 4.9,
        "mentor": "Vikram Rao",
        "short_description": "A challenging trek through the Western Ghats.",
        "description": "Kumara Parvatha is one of Karnataka's most challenging and rewarding treks, offering spectacular Western Ghats scenery."
    },

    "Kodachadri": {
        "name": "Kodachadri",
        "location": "Shivamogga",
        "image": "kodachadri.png",
        "difficulty": "Moderate",
        "duration": "2 Days",
        "distance": "14 km",
        "elevation": "1,343 m",
        "price": 1299,
        "rating": 4.8,
        "mentor": "Naveen Kumar",
        "short_description": "A misty mountain trek surrounded by dense forests.",
        "description": "Kodachadri is famous for its lush forests, mountain views, sunset points and beautiful mist-covered landscapes."
    },

    "Tadiandamol": {
        "name": "Tadiandamol",
        "location": "Coorg",
        "image": "tadiandamol.png",
        "difficulty": "Moderate",
        "duration": "1 Day",
        "distance": "8 km",
        "elevation": "1,748 m",
        "price": 999,
        "rating": 4.7,
        "mentor": "Kiran Raj",
        "short_description": "A scenic high-altitude trek in Coorg.",
        "description": "Tadiandamol is the highest peak in Coorg and provides beautiful views of the Western Ghats."
    },

    "Mullayanagiri": {
        "name": "Mullayanagiri",
        "location": "Chikkamagaluru",
        "image": "mullayanagiri.png",
        "difficulty": "Easy",
        "duration": "1 Day",
        "distance": "5 km",
        "elevation": "1,930 m",
        "price": 799,
        "rating": 4.8,
        "mentor": "Aditya Kumar",
        "short_description": "A short trek to Karnataka's highest peak.",
        "description": "Mullayanagiri is the highest peak in Karnataka and is famous for panoramic mountain views."
    },

    "Brahmagiri": {
        "name": "Brahmagiri",
        "location": "Coorg",
        "image": "brahmagiri.png",
        "difficulty": "Moderate",
        "duration": "2 Days",
        "distance": "10 km",
        "elevation": "1,608 m",
        "price": 1399,
        "rating": 4.6,
        "mentor": "Manoj Bhat",
        "short_description": "A forest trek filled with beautiful Western Ghats scenery.",
        "description": "Brahmagiri offers a peaceful trekking experience through forests, grasslands and mountain terrain."
    },

    "Nandi Hills": {
        "name": "Nandi Hills",
        "location": "Chikkaballapur",
        "image": "nandi-hills.png",
        "difficulty": "Easy",
        "duration": "1 Day",
        "distance": "4 km",
        "elevation": "1,478 m",
        "price": 599,
        "rating": 4.5,
        "mentor": "Rohit Sharma",
        "short_description": "An easy and popular hill trek near Bengaluru.",
        "description": "Nandi Hills is a popular destination for sunrise views, cycling, hiking and weekend trips."
    },

    "Savandurga": {
        "name": "Savandurga",
        "location": "Bengaluru",
        "image": "savandurga.png",
        "difficulty": "Moderate",
        "duration": "1 Day",
        "distance": "5 km",
        "elevation": "1,226 m",
        "price": 699,
        "rating": 4.6,
        "mentor": "Suresh Gowda",
        "short_description": "A rocky hill trek close to Bengaluru.",
        "description": "Savandurga is one of Asia's largest monolith hills and is a popular trekking destination near Bengaluru."
    },

    "Ettina Bhuja": {
        "name": "Ettina Bhuja",
        "location": "Dakshina Kannada",
        "image": "ettina-bhuja.png",
        "difficulty": "Moderate",
        "duration": "1 Day",
        "distance": "7 km",
        "elevation": "1,300 m",
        "price": 1199,
        "rating": 4.8,
        "mentor": "Deepak Kumar",
        "short_description": "A scenic Western Ghats trekking destination.",
        "description": "Ettina Bhuja offers beautiful grasslands, mountain views and peaceful trekking trails."
    },

    "Kunti Betta": {
        "name": "Kunti Betta",
        "location": "Mandya",
        "image": "kunti-betta.png",
        "difficulty": "Easy",
        "duration": "1 Day",
        "distance": "4 km",
        "elevation": "878 m",
        "price": 699,
        "rating": 4.6,
        "mentor": "Prakash R",
        "short_description": "A short rocky trek famous for sunrise and camping.",
        "description": "Kunti Betta is a popular destination for night trekking, sunrise views and outdoor activities."
    },

    "Ballalarayana Durga": {
        "name": "Ballalarayana Durga",
        "location": "Chikkamagaluru",
        "image": "ballalarayana-durga.png",
        "difficulty": "Moderate",
        "duration": "1 Day",
        "distance": "6 km",
        "elevation": "1,509 m",
        "price": 1099,
        "rating": 4.7,
        "mentor": "Harish Kumar",
        "short_description": "A beautiful trek leading to historic fort ruins.",
        "description": "Ballalarayana Durga combines mountain trekking with historical exploration and spectacular Western Ghats views."
    }
}


# =========================================================
# ACTIVE TREKS
# =========================================================

treks = {}


# =========================================================
# HELPER - CHECK FILE EXTENSION
# =========================================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================================================
# HELPER - PRICE CONVERSION
# =========================================================

def price_to_number(price):

    try:

        return int(
            float(
                str(price)
                .replace(",", "")
                .replace("₹", "")
                .strip()
            )
        )

    except:

        return 0


# =========================================================
# HELPER - FIND TREK BY NAME
# =========================================================
# This helper solves trek-name matching problems.
#
# It handles:
# - spaces
# - URL encoding
# - uppercase/lowercase differences
# - treks added from Admin
# =========================================================

def find_trek_by_name(trek_name):

    if trek_name is None:
        return None

    # Decode URL value
    decoded_name = unquote_plus(
        str(trek_name)
    ).strip()

    # Search through all loaded treks
    for trek in treks.values():

        current_name = str(
            trek.get("name", "")
        ).strip()

        if current_name.lower() == decoded_name.lower():

            return trek

    return None


# =========================================================
# SAVE DEFAULT TREKS TO DATABASE
# =========================================================

def save_default_treks_to_database():

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            print(
                "Database connection failed while checking treks."
            )

            return

        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM treks"
        )

        count = cursor.fetchone()[0]

        if count > 0:

            print(
                f"Treks already exist in database: {count}"
            )

            return

        print("No treks found in database.")
        print("Adding default treks...")

        query = """
        INSERT INTO treks (
            trek_name,
            location,
            image,
            difficulty,
            duration,
            distance,
            elevation,
            price,
            rating,
            mentor,
            short_description,
            description
        )
        VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
        """

        for trek in default_treks.values():

            values = (
                trek["name"],
                trek["location"],
                trek["image"],
                trek["difficulty"],
                trek["duration"],
                trek["distance"],
                trek["elevation"],
                trek["price"],
                trek["rating"],
                trek["mentor"],
                trek["short_description"],
                trek["description"]
            )

            cursor.execute(
                query,
                values
            )

        connection.commit()

        print(
            f"Default treks inserted successfully: "
            f"{len(default_treks)}"
        )

    except Exception as e:

        print(
            "Default trek database error:",
            e
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# LOAD TREKS FROM DATABASE
# =========================================================

def load_treks_from_database():

    global treks

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            print("Could not connect to database.")
            print("Using default trek data.")

            treks = default_treks.copy()

            return

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT
                id,
                trek_name,
                location,
                image,
                difficulty,
                duration,
                distance,
                elevation,
                price,
                rating,
                mentor,
                short_description,
                description
            FROM treks
            ORDER BY id ASC
        """)

        rows = cursor.fetchall()

        treks = {}

        for row in rows:

            trek_name = row["trek_name"]

            treks[trek_name] = {

                "id": row["id"],

                "name": row["trek_name"],

                "location": row["location"] or "",

                "image": row["image"] or "",

                "difficulty": row["difficulty"] or "",

                "duration": row["duration"] or "",

                "distance": row["distance"] or "",

                "elevation": row["elevation"] or "",

                "price": price_to_number(
                    row["price"]
                ),

                "rating": float(
                    row["rating"] or 0
                ),

                "mentor": row["mentor"] or "",

                "short_description":
                    row["short_description"] or "",

                "description":
                    row["description"] or ""
            }

        print(
            f"Treks loaded from database: {len(treks)}"
        )

    except Exception as e:

        print(
            "Trek loading error:",
            e
        )

        treks = default_treks.copy()

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# GET TREKS FOR ADMIN DASHBOARD
# =========================================================

def get_admin_treks():

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            print(
                "Admin trek database connection failed."
            )

            return []

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT
                id,
                trek_name,
                location,
                image,
                difficulty,
                duration,
                distance,
                elevation,
                price,
                rating,
                mentor,
                short_description,
                description
            FROM treks
            ORDER BY id ASC
        """)

        rows = cursor.fetchall()

        admin_treks = []

        for row in rows:

            admin_treks.append({

                "id": row["id"],

                "name": row["trek_name"],

                "location": row["location"] or "",

                "image": row["image"] or "",

                "difficulty": row["difficulty"] or "",

                "duration": row["duration"] or "",

                "distance": row["distance"] or "",

                "elevation": row["elevation"] or "",

                "price": price_to_number(
                    row["price"]
                ),

                "rating": float(
                    row["rating"] or 0
                ),

                "mentor": row["mentor"] or "",

                "short_description":
                    row["short_description"] or "",

                "description":
                    row["description"] or ""
            })

        print(
            f"Admin dashboard treks fetched: "
            f"{len(admin_treks)}"
        )

        return admin_treks

    except Exception as e:

        print(
            "Admin trek fetch error:",
            e
        )

        return []

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    load_treks_from_database()

    return render_template(
        "index.html",
        treks=treks
    )


# =========================================================
# CATEGORY PAGE
# =========================================================

@app.route("/category/<category>")
def category(category):

    load_treks_from_database()

    category_treks = {}

    category_lower = category.lower()

    for name, trek in treks.items():

        if (
            trek["difficulty"].lower()
            == category_lower
        ):

            category_treks[name] = trek

    return render_template(
        "category.html",
        category=category,
        treks=category_treks
    )


# =========================================================
# TREK DETAILS
# =========================================================

@app.route("/trek/<path:trek_name>")
def trek_details(trek_name):

    load_treks_from_database()

    trek = find_trek_by_name(
        trek_name
    )

    if trek is None:

        print(
            "Trek details not found:",
            trek_name
        )

        print(
            "Available treks:",
            list(treks.keys())
        )

        return "Trek not found", 404

    return render_template(
        "trek_details.html",
        trek=trek
    )


# =========================================================
# BOOKING PAGE
# =========================================================

@app.route("/book/<path:trek_name>")
def booking_page(trek_name):

    # =====================================================
    # CHECK WHETHER CUSTOMER IS LOGGED IN
    # =====================================================

    if not session.get("user_id"):

        return redirect(
            url_for(
                "login",
                next=url_for(
                    "booking_page",
                    trek_name=trek_name
                )
            )
        )

    print(
        "Booking requested for:",
        trek_name
    )

    # =====================================================
    # LOAD LATEST TREK DATA
    # =====================================================

    load_treks_from_database()

    # =====================================================
    # FIND TREK SAFELY
    # =====================================================

    selected_trek = find_trek_by_name(
        trek_name
    )

    # =====================================================
    # TREK NOT FOUND
    # =====================================================

    if selected_trek is None:

        print(
            "Booking trek not found:",
            trek_name
        )

        print(
            "Available treks:",
            list(treks.keys())
        )

        return f"""
        <!DOCTYPE html>

        <html>

        <head>

            <title>Trek Not Found | Trekora</title>

            <style>

                * {{
                    box-sizing: border-box;
                }}

                body {{
                    margin: 0;
                    font-family: Arial, sans-serif;
                    background: #f4f7f5;

                    display: flex;
                    align-items: center;
                    justify-content: center;

                    min-height: 100vh;
                }}

                .box {{
                    width: 90%;
                    max-width: 550px;

                    background: white;

                    padding: 45px;

                    border-radius: 20px;

                    text-align: center;

                    box-shadow:
                        0 15px 40px
                        rgba(0,0,0,0.08);
                }}

                .icon {{
                    font-size: 55px;
                    margin-bottom: 15px;
                }}

                h1 {{
                    color: #23463a;
                    margin-bottom: 10px;
                }}

                p {{
                    color: #66756d;
                    line-height: 1.7;
                }}

                .button {{
                    display: inline-block;

                    margin-top: 20px;

                    padding: 13px 25px;

                    background: #4c9f32;

                    color: white;

                    text-decoration: none;

                    border-radius: 10px;

                    font-weight: bold;
                }}

                .button:hover {{
                    background: #3d8628;
                }}

            </style>

        </head>

        <body>

            <div class="box">

                <div class="icon">
                    🔍
                </div>

                <h1>
                    Trek Not Found
                </h1>

                <p>
                    We could not find the trek
                    <strong>{trek_name}</strong>.
                </p>

                <a
                    href="/"
                    class="button"
                >
                    ← Back to Trekora
                </a>

            </div>

        </body>

        </html>
        """, 404

    # =====================================================
    # GET MAXIMUM TRAVELLERS FROM ADMIN SETTINGS
    # =====================================================

    max_travellers = get_admin_setting(
        "max_travellers",
        "10"
    )

    # =====================================================
    # CONVERT SETTING TO INTEGER
    # =====================================================

    try:

        max_travellers = int(
            max_travellers
        )

    except:

        max_travellers = 10

    # =====================================================
    # SAFETY CHECK
    # =====================================================

    if max_travellers < 1:

        max_travellers = 1

    # =====================================================
    # SHOW CURRENT VALUE IN TERMINAL
    # =====================================================

    print(
        "Maximum travellers allowed:",
        max_travellers
    )

    # =====================================================
    # OPEN BOOKING PAGE
    # =====================================================

    return render_template(
        "booking.html",
        trek=selected_trek,
        max_travellers=max_travellers
    )

# =========================================================
# SUBMIT BOOKING
# =========================================================

# =========================================================
# SUBMIT BOOKING
# =========================================================

@app.route(
    "/submit-booking",
    methods=["POST"]
)
def submit_booking():

    # =====================================================
    # CHECK WHETHER NEW BOOKINGS ARE ALLOWED
    # =====================================================

    allow_bookings = get_admin_setting(
        "allow_bookings",
        "true"
    )

    if str(allow_bookings).lower() != "true":

        return """
        <!DOCTYPE html>

        <html>

        <head>

            <title>Bookings Temporarily Closed | Trekora</title>

            <style>

                body {
                    margin: 0;
                    font-family: Arial, sans-serif;
                    background: #f4f7f5;

                    display: flex;
                    justify-content: center;
                    align-items: center;

                    min-height: 100vh;
                }

                .box {
                    width: 90%;
                    max-width: 550px;

                    background: white;

                    padding: 45px;

                    border-radius: 20px;

                    text-align: center;

                    box-shadow:
                        0 15px 40px
                        rgba(0,0,0,0.08);
                }

                .icon {
                    font-size: 50px;
                    margin-bottom: 15px;
                }

                h1 {
                    color: #23463a;
                    margin-bottom: 12px;
                }

                p {
                    color: #66756d;
                    line-height: 1.7;
                }

                .button {
                    display: inline-block;

                    margin-top: 20px;

                    padding: 13px 25px;

                    background: #287a4b;

                    color: white;

                    text-decoration: none;

                    border-radius: 10px;

                    font-weight: bold;
                }

            </style>

        </head>

        <body>

            <div class="box">

                <div class="icon">
                    📅
                </div>

                <h1>
                    Bookings Temporarily Closed
                </h1>

                <p>
                    New trek bookings are currently unavailable.
                    Please check back later.
                </p>

                <a
                    href="/"
                    class="button"
                >
                    ← Back to Trekora
                </a>

            </div>

        </body>

        </html>
        """, 403

    # =====================================================
    # GET BOOKING FORM DATA
    # =====================================================

    trek_name = request.form.get(
        "trek_name",
        ""
    ).strip()

    name = request.form.get(
        "name",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip()

    phone = request.form.get(
        "phone",
        ""
    ).strip()

    payment_method = request.form.get(
        "payment_method",
        ""
    ).strip()

    trek_date = request.form.get(
        "trek_date",
        ""
    ).strip()

    people = request.form.get(
        "people",
        "1"
    ).strip()

    experience = request.form.get(
        "experience",
        ""
    ).strip()

    emergency_name = request.form.get(
        "emergency_name",
        ""
    ).strip()

    emergency_phone = request.form.get(
        "emergency_phone",
        ""
    ).strip()

    # =====================================================
    # CHECK PAYMENT METHOD
    # =====================================================

    if payment_method not in [
        "UPI",
        "Credit Card",
        "Debit Card",
        "Net Banking",
        "Cash"
    ]:

        return (
            "Please select a valid payment method.",
            400
        )

    # =====================================================
    # LOAD LATEST TREK DATA
    # =====================================================

    load_treks_from_database()

    # =====================================================
    # FIND TREK SAFELY
    # =====================================================

    trek = find_trek_by_name(
        trek_name
    )

    if trek is None:

        print(
            "Submit booking trek not found:",
            trek_name
        )

        return "Trek not found", 404

    # =====================================================
    # USE EXACT TREK NAME FROM DATABASE
    # =====================================================

    trek_name = trek["name"]

    # =====================================================
    # CONVERT NUMBER OF PEOPLE
    # =====================================================

    try:

        people = int(
            people
        )

    except:

        people = 1

    if people < 1:

        people = 1

    # =====================================================
    # CHECK MAXIMUM TRAVELLERS ALLOWED
    # =====================================================

    max_travellers = get_admin_setting(
        "max_travellers",
        "10"
    )

    try:

        max_travellers = int(
            max_travellers
        )

    except:

        max_travellers = 10

    if people > max_travellers:

        return f"""
        <!DOCTYPE html>

        <html>

        <head>

            <title>Booking Limit | Trekora</title>

            <style>

                body {{
                    margin: 0;
                    font-family: Arial, sans-serif;
                    background: #f4f7f5;

                    display: flex;
                    justify-content: center;
                    align-items: center;

                    min-height: 100vh;
                }}

                .box {{
                    width: 90%;
                    max-width: 550px;

                    background: white;

                    padding: 45px;

                    border-radius: 20px;

                    text-align: center;

                    box-shadow:
                        0 15px 40px
                        rgba(0,0,0,0.08);
                }}

                .icon {{
                    width: 70px;
                    height: 70px;

                    margin: auto;

                    border-radius: 50%;

                    background: #fff4e5;

                    color: #b26a00;

                    display: flex;

                    align-items: center;
                    justify-content: center;

                    font-size: 32px;
                }}

                h1 {{
                    color: #23463a;
                    margin-top: 20px;
                }}

                p {{
                    color: #66756d;
                    line-height: 1.7;
                }}

                .button {{
                    display: inline-block;

                    margin-top: 20px;

                    padding: 13px 25px;

                    background: #287a4b;

                    color: white;

                    text-decoration: none;

                    border-radius: 10px;

                    font-weight: bold;
                }}

            </style>

        </head>

        <body>

            <div class="box">

                <div class="icon">
                    !
                </div>

                <h1>
                    Traveller Limit Exceeded
                </h1>

                <p>
                    This booking allows a maximum of
                    <strong>{max_travellers}</strong>
                    travellers.
                </p>

                <p>
                    Please reduce the number of travellers
                    and try again.
                </p>

                <a
                    href="javascript:history.back()"
                    class="button"
                >
                    ← Back to Booking
                </a>

            </div>

        </body>

        </html>
        """, 400

    # =====================================================
    # CALCULATE PRICE
    # =====================================================

    price_per_person = price_to_number(
        trek["price"]
    )

    total_amount = (
        price_per_person * people
    )

    # =====================================================
    # GENERATE BOOKING ID
    # =====================================================

    booking_id = (
        "TRK-"
        + uuid.uuid4().hex[:8].upper()
    )

    # =====================================================
    # SAVE BOOKING
    # =====================================================

    success = save_booking(
        session.get("user_id"),
        booking_id,
        trek_name,
        name,
        email,
        phone,
        trek_date,
        people,
        experience,
        emergency_name,
        emergency_phone,
        price_per_person,
        total_amount,
        payment_method
    )

    if not success:

        return """
        <h2>Booking could not be completed</h2>
        <p>Please try again.</p>
        <a href="/">Back to Home</a>
        """, 500


    # ==========================================
    # NEW BOOKING NOTIFICATION
    # ==========================================

    booking_notifications = get_admin_setting(
        "booking_notifications",
        "true"
    )

    if str(
        booking_notifications
    ).lower() == "true":

        notification_created = create_notification(
            None,
            "booking",
            "New Booking Received",
            (
                f"{name} booked "
                f"{trek_name} for "
                f"{people} traveller(s)."
            ),
            booking_id
        )

        print(
            "New booking notification created:",
            booking_id
        )

        print(
            "Notification insert result:",
            notification_created
        )
    # =====================================================
    # BOOKING SUCCESS PAGE
    # =====================================================

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>Booking Confirmed - Trekora</title>

        <style>

            body {{
                margin: 0;

                font-family: Arial, sans-serif;

                background: #f4f7f5;

                display: flex;

                justify-content: center;

                align-items: center;

                min-height: 100vh;
            }}

            .box {{
                width: 90%;

                max-width: 650px;

                background: white;

                border-radius: 18px;

                padding: 45px;

                text-align: center;

                box-shadow:
                    0 15px 45px
                    rgba(0,0,0,0.08);
            }}

            .success {{
                width: 70px;

                height: 70px;

                margin: auto;

                border-radius: 50%;

                background: #e7f6ed;

                color: #287a4b;

                display: flex;

                align-items: center;

                justify-content: center;

                font-size: 36px;
            }}

            h1 {{
                color: #23463a;

                margin-top: 20px;
            }}

            .booking-id {{
                background: #f0f7f3;

                padding: 15px;

                border-radius: 10px;

                margin: 20px 0;

                font-weight: bold;

                color: #287a4b;
            }}

            .details {{
                text-align: left;

                margin-top: 25px;

                line-height: 1.9;
            }}

            .details strong {{
                color: #294238;
            }}

            .button {{
                display: inline-block;

                margin-top: 25px;

                padding: 13px 25px;

                background: #287a4b;

                color: white;

                text-decoration: none;

                border-radius: 9px;
            }}

        </style>

    </head>

    <body>

        <div class="box">

            <div class="success">
                ✓
            </div>

            <h1>
                Booking Confirmed!
            </h1>

            <p>
                Your trek reservation has been successfully submitted.
            </p>

            <div class="booking-id">

                Booking ID:
                {booking_id}

            </div>

            <div class="details">

                <strong>Trek:</strong>
                {trek_name}

                <br>

                <strong>Name:</strong>
                {name}

                <br>

                <strong>Email:</strong>
                {email}

                <br>

                <strong>Phone:</strong>
                {phone}

                <br>

                <strong>Date:</strong>
                {trek_date}

                <br>

                <strong>People:</strong>
                {people}

                <br>

                <strong>Experience:</strong>
                {experience}

                <br>

                <strong>Total Amount:</strong>
                ₹{total_amount:,}

            </div>

            <a
                href="/"
                class="button"
            >
                Back to Trekora
            </a>

        </div>

    </body>

    </html>
    """

# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def admin_login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        if (
            username == "admin"
            and password == "admin123"
        ):

            session["admin_logged_in"] = True

            return redirect(
                url_for("admin_dashboard")
            )
        
        return render_template(
            "admin_login.html",
            error="Invalid username or password."
        )

    return render_template(
        "admin_login.html"
    )


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin/logout")
def admin_logout():

    session.clear()

    return redirect(
        url_for("admin_login")
    )

# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin")
def admin_dashboard():

    if not session.get("admin_logged_in"):
        
        return redirect(
            url_for("admin_login")
        )

    connection = None
    cursor = None

    bookings = []
    users = []
    mentors = []

    total_bookings = 0
    total_people = 0
    total_revenue = 0

    pending_bookings = 0
    confirmed_bookings = 0
    cancelled_bookings = 0

    # =====================================================
    # PAYMENT STATISTICS
    # =====================================================

    total_payments = 0
    paid_payments = 0
    pending_payments = 0
    refunded_payments = 0
    total_paid_amount = 0

    try:

        connection = get_db_connection()

        if connection is None:

            print(
                "Could not connect to database "
                "for admin dashboard."
            )

        else:

            cursor = connection.cursor(
                dictionary=True
            )

            # =================================================
            # FETCH BOOKINGS
            # =================================================

            cursor.execute("""
                SELECT *
                FROM bookings
                ORDER BY created_at DESC
            """)

            bookings = cursor.fetchall()

            total_bookings = len(bookings)

            # =================================================
            # TOTAL PEOPLE
            # =================================================

            for booking in bookings:

                try:

                    total_people += int(
                        booking.get("people") or 0
                    )

                except:

                    pass

            # =================================================
            # TOTAL REVENUE
            # =================================================

            for booking in bookings:

                status = (
                    booking.get("status")
                    or ""
                ).strip().lower()

                if status != "cancelled":

                    try:

                        total_revenue += float(
                            booking.get(
                                "total_amount"
                            ) or 0
                        )

                    except:

                        pass

            # =================================================
            # BOOKING STATUS COUNTS
            # =================================================

            for booking in bookings:

                status = (
                    booking.get("status")
                    or ""
                ).strip().lower()

                if status == "pending":

                    pending_bookings += 1

                elif status == "confirmed":

                    confirmed_bookings += 1

                elif status == "cancelled":

                    cancelled_bookings += 1

            # =================================================
            # PAYMENT STATISTICS
            # =================================================

            total_payments = len(bookings)

            paid_payments = 0
            pending_payments = 0
            refunded_payments = 0
            total_paid_amount = 0

            for booking in bookings:

                payment_status = (
                    booking.get("payment_status")
                    or "Pending"
                ).strip().lower()

                if payment_status == "paid":

                    paid_payments += 1

                    try:

                        total_paid_amount += float(
                            booking.get(
                                "total_amount"
                            ) or 0
                        )

                    except:

                        pass

                elif payment_status == "refunded":

                    refunded_payments += 1

                else:

                    pending_payments += 1

    except Exception as e:

        print(
            "Admin dashboard booking error:",
            e
        )

    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


    # =========================================================
    # FETCH TREKS
    # =========================================================

    admin_treks = get_admin_treks()

    print(
        "Sending treks to admin.html:",
        len(admin_treks)
    )


    # =========================================================
    # FETCH USERS
    # =========================================================

    users = get_all_users()

    print(
        "Sending users to admin.html:",
        len(users)
    )


    # =========================================================
    # FETCH MENTORS
    # =========================================================

    mentors = get_all_mentors()

    print(
        "Sending mentors to admin.html:",
        len(mentors)
    )
    notifications = get_notifications(
    None,
    20
)

    # =========================================================
    # RENDER ADMIN DASHBOARD
    # =========================================================

    return render_template(

        "admin.html",

        bookings=bookings,

        treks=admin_treks,

        users=users,

        mentors=mentors,

        notifications=notifications,

        total_bookings=total_bookings,

        total_people=total_people,

        total_revenue=total_revenue,

        pending_bookings=pending_bookings,

        confirmed_bookings=confirmed_bookings,

        cancelled_bookings=cancelled_bookings,

        total_payments=total_payments,

        paid_payments=paid_payments,

        pending_payments=pending_payments,

        refunded_payments=refunded_payments,

        total_paid_amount=total_paid_amount
    )

# =========================================================
# ADMIN URL ALIAS
# =========================================================

app.add_url_rule(
    "/admin",
    endpoint="admin",
    view_func=admin_dashboard
)
# =========================================================
# ADMIN USER DETAILS
# =========================================================

# =========================================================
# ADMIN USER DETAILS
# =========================================================

@app.route("/admin/user/<int:user_id>")
def admin_user_details(user_id):

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )

    connection = None
    cursor = None

    user = None
    bookings = []

    try:

        connection = get_db_connection()

        if connection is None:

            return "Database connection failed.", 500

        cursor = connection.cursor(
            dictionary=True
        )


        # =================================================
        # GET USER DETAILS
        # =================================================

        cursor.execute("""
            SELECT
                id,
                name,
                email,
                phone,
                created_at
            FROM users
            WHERE id = %s
        """, (user_id,))

        user = cursor.fetchone()


        # =================================================
        # USER NOT FOUND
        # =================================================

        if not user:

            return """
            <script>
                alert("User not found.");
                window.location.href = "/admin#users";
            </script>
            """


        # =================================================
        # GET USER BOOKINGS
        # =================================================

        cursor.execute("""
            SELECT
                id,
                booking_id,
                trek_name,
                name,
                email,
                phone,
                trek_date,
                people,
                experience,
                price_per_person,
                total_amount,
                status,
                payment_status,
                payment_method,
                payment_date,
                created_at
            FROM bookings
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (user_id,))

        bookings = cursor.fetchall()


        print(
            "User bookings loaded:",
            len(bookings)
        )


        # =================================================
        # RENDER USER DETAILS
        # =================================================

        return render_template(
            "user_details.html",
            user=user,
            bookings=bookings
        )


    except Exception as e:

        print(
            "Admin User Details Error:",
            e
        )

        return """
        <script>
            alert("Unable to load user details.");
            window.location.href = "/admin#users";
        </script>
        """


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# =========================================================
# ADMIN PAYMENT DETAILS
# =========================================================

@app.route("/admin/payment/<booking_id>")
def admin_payment_details(booking_id):

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            return "Database connection failed.", 500

        cursor = connection.cursor(
            dictionary=True
        )


        # =================================================
        # GET PAYMENT / BOOKING DETAILS
        # =================================================

        cursor.execute("""
            SELECT
                id,
                user_id,
                booking_id,
                trek_name,
                name,
                email,
                phone,
                trek_date,
                people,
                experience,
                emergency_name,
                emergency_phone,
                price_per_person,
                total_amount,
                status,
                payment_status,
                payment_method,
                payment_date,
                created_at
            FROM bookings
            WHERE booking_id = %s
        """, (booking_id,))

        payment = cursor.fetchone()


        # =================================================
        # PAYMENT NOT FOUND
        # =================================================

        if not payment:

            return """
            <script>
                alert("Payment record not found.");
                window.location.href = "/admin#payments";
            </script>
            """


        # =================================================
        # RENDER PAYMENT DETAILS
        # =================================================

        return render_template(
            "payment_details.html",
            payment=payment
        )


    except Exception as e:

        print(
            "Admin Payment Details Error:",
            e
        )

        return """
        <script>
            alert("Unable to load payment details.");
            window.location.href = "/admin#payments";
        </script>
        """


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# =========================================================
# DELETE USER
# =========================================================

@app.route("/admin/delete-user/<int:user_id>", methods=["POST"])
def delete_user(user_id):

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            return """
            <script>
                alert("Database connection failed.");
                window.location.href = "/admin#users";
            </script>
            """

        cursor = connection.cursor(
            dictionary=True
        )

        # =================================================
        # CHECK USER EXISTS
        # =================================================

        cursor.execute("""
            SELECT
                id,
                name
            FROM users
            WHERE id = %s
        """, (user_id,))

        user = cursor.fetchone()

        if not user:

            return """
            <script>
                alert("User not found.");
                window.location.href = "/admin#users";
            </script>
            """


        # =================================================
        # DELETE USER
        # =================================================

        cursor.execute("""
            DELETE FROM users
            WHERE id = %s
        """, (user_id,))

        connection.commit()


        print(
            "User deleted successfully:",
            user["name"]
        )


        # =================================================
        # RETURN TO USERS
        # =================================================

        return redirect(
            url_for("admin_dashboard")
            + "#users"
        )


    except Exception as e:

        print(
            "Delete User Error:",
            e
        )

        if connection:

            connection.rollback()

        return """
        <script>
            alert("Unable to delete user. Please try again.");
            window.location.href = "/admin#users";
        </script>
        """


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# =========================================================
# EDIT USER
# =========================================================

@app.route("/admin/edit-user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            return "Database connection failed.", 500

        cursor = connection.cursor(
            dictionary=True
        )

        # =================================================
        # GET USER
        # =================================================

        cursor.execute("""
            SELECT
                id,
                name,
                email,
                phone,
                created_at
            FROM users
            WHERE id = %s
        """, (user_id,))

        user = cursor.fetchone()


        # =================================================
        # USER NOT FOUND
        # =================================================

        if not user:

            return """
            <script>
                alert("User not found.");
                window.location.href = "/admin#users";
            </script>
            """


        # =================================================
        # SHOW EDIT FORM
        # =================================================

        if request.method == "GET":

            return render_template(
                "edit_user.html",
                user=user
            )


        # =================================================
        # GET UPDATED DETAILS
        # =================================================

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()


        # =================================================
        # VALIDATION
        # =================================================

        if not name:

            return """
            <script>
                alert("User name is required.");
                window.history.back();
            </script>
            """

        if not email:

            return """
            <script>
                alert("Email address is required.");
                window.history.back();
            </script>
            """


        # =================================================
        # UPDATE USER
        # =================================================

        cursor.execute("""
            UPDATE users
            SET
                name = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (
            name,
            email,
            phone,
            user_id
        ))

        connection.commit()


        print(
            "User updated successfully:",
            user_id
        )


        # =================================================
        # RETURN TO USERS
        # =================================================

        return redirect(
            url_for("admin_dashboard")
            + "#users"
        )


    except Exception as e:

        print(
            "Edit User Error:",
            e
        )

        if connection:

            connection.rollback()

        return """
        <script>
            alert("Unable to update user. Please try again.");
            window.history.back();
        </script>
        """


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# =========================================================
# MENTOR MANAGEMENT
# =========================================================

@app.route("/admin/mentor/<int:mentor_id>")
def mentor_management(mentor_id):

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            return "Database connection failed.", 500

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT
                id,
                name,
                phone,
                email,
                experience,
                specialization,
                status,
                created_at
            FROM mentors
            WHERE id = %s
        """, (mentor_id,))

        mentor = cursor.fetchone()

        if not mentor:

            return """
                <script>
                    alert("Mentor not found.");
                    window.location.href="/admin#mentors";
                </script>
            """

        return render_template(
            "mentor_management.html",
            mentor=mentor
        )

    except Exception as e:

        print(
            "Mentor Management Error:",
            e
        )

        return "Something went wrong while loading the mentor.", 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# ADD MENTOR
# =========================================================

@app.route("/admin/add-mentor", methods=["GET", "POST"])
def add_mentor():

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )

    # =====================================================
    # SHOW ADD MENTOR FORM
    # =====================================================

    if request.method == "GET":

        return render_template(
            "add_mentor.html"
        )

    # =====================================================
    # GET FORM DATA
    # =====================================================

    name = request.form.get(
        "name",
        ""
    ).strip()

    phone = request.form.get(
        "phone",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip()

    experience = request.form.get(
        "experience",
        "0"
    ).strip()

    specialization = request.form.get(
        "specialization",
        ""
    ).strip()

    status = request.form.get(
        "status",
        "Active"
    ).strip()


    # =====================================================
    # VALIDATION
    # =====================================================

    if not name:

        return """
        <script>
            alert("Mentor name is required.");
            window.history.back();
        </script>
        """


    try:

        experience = int(
            experience or 0
        )

    except ValueError:

        experience = 0


    # =====================================================
    # SAVE MENTOR
    # =====================================================

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            return """
            <script>
                alert("Database connection failed.");
                window.history.back();
            </script>
            """


        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO mentors
            (
                name,
                phone,
                email,
                experience,
                specialization,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """, (
            name,
            phone,
            email,
            experience,
            specialization,
            status
        ))


        connection.commit()


        print(
            "Mentor added successfully:",
            name
        )


        return redirect(
            url_for("admin_dashboard")
            + "#mentors"
        )


    except Exception as e:

        print(
            "Add Mentor Error:",
            e
        )

        if connection:

            connection.rollback()


        return """
        <script>
            alert("Unable to add mentor. Please try again.");
            window.history.back();
        </script>
        """


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()



# =========================================================
# EDIT MENTOR
# =========================================================

@app.route("/admin/edit-mentor/<int:mentor_id>", methods=["GET", "POST"])
def edit_mentor(mentor_id):

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            return "Database connection failed.", 500

        cursor = connection.cursor(
            dictionary=True
        )

        # =================================================
        # GET MENTOR
        # =================================================

        cursor.execute("""
            SELECT
                id,
                name,
                phone,
                email,
                experience,
                specialization,
                status,
                created_at
            FROM mentors
            WHERE id = %s
        """, (mentor_id,))

        mentor = cursor.fetchone()

        if not mentor:

            return """
            <script>
                alert("Mentor not found.");
                window.location.href = "/admin#mentors";
            </script>
            """


        # =================================================
        # SHOW EDIT FORM
        # =================================================

        if request.method == "GET":

            return render_template(
                "edit_mentor.html",
                mentor=mentor
            )


        # =================================================
        # GET UPDATED DETAILS
        # =================================================

        name = request.form.get(
            "name",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        experience = request.form.get(
            "experience",
            "0"
        ).strip()

        specialization = request.form.get(
            "specialization",
            ""
        ).strip()

        status = request.form.get(
            "status",
            "Active"
        ).strip()


        # =================================================
        # VALIDATION
        # =================================================

        if not name:

            return """
            <script>
                alert("Mentor name is required.");
                window.history.back();
            </script>
            """


        try:

            experience = int(
                experience or 0
            )

        except ValueError:

            experience = 0


        # =================================================
        # UPDATE MENTOR
        # =================================================

        cursor.execute("""
            UPDATE mentors
            SET
                name = %s,
                phone = %s,
                email = %s,
                experience = %s,
                specialization = %s,
                status = %s
            WHERE id = %s
        """, (
            name,
            phone,
            email,
            experience,
            specialization,
            status,
            mentor_id
        ))


        connection.commit()


        print(
            "Mentor updated successfully:",
            mentor_id
        )


        return redirect(
            url_for("admin_dashboard")
            + "#mentors"
        )


    except Exception as e:

        print(
            "Edit Mentor Error:",
            e
        )

        if connection:

            connection.rollback()

        return """
        <script>
            alert("Unable to update mentor. Please try again.");
            window.history.back();
        </script>
        """


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# =========================================================
# DELETE MENTOR
# =========================================================

@app.route("/admin/delete-mentor/<int:mentor_id>", methods=["POST"])
def delete_mentor(mentor_id):

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            return """
            <script>
                alert("Database connection failed.");
                window.location.href = "/admin#mentors";
            </script>
            """

        cursor = connection.cursor(
            dictionary=True
        )

        # =================================================
        # CHECK MENTOR EXISTS
        # =================================================

        cursor.execute("""
            SELECT
                id,
                name
            FROM mentors
            WHERE id = %s
        """, (mentor_id,))

        mentor = cursor.fetchone()

        if not mentor:

            return """
            <script>
                alert("Mentor not found.");
                window.location.href = "/admin#mentors";
            </script>
            """


        # =================================================
        # DELETE MENTOR
        # =================================================

        cursor.execute("""
            DELETE FROM mentors
            WHERE id = %s
        """, (mentor_id,))

        connection.commit()


        print(
            "Mentor deleted successfully:",
            mentor["name"]
        )


        # =================================================
        # RETURN TO MENTORS SECTION
        # =================================================

        return redirect(
            url_for("admin_dashboard")
            + "#mentors"
        )


    except Exception as e:

        print(
            "Delete Mentor Error:",
            e
        )

        if connection:

            connection.rollback()

        return """
        <script>
            alert("Unable to delete mentor. Please try again.");
            window.location.href = "/admin#mentors";
        </script>
        """


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()

            
# =========================================================
# ADMIN BOOKING DETAILS
# =========================================================

@app.route(
    "/admin/booking/<booking_id>"
)
def admin_booking_details(
    booking_id
):

    if not session.get(
        "admin_logged_in"
    ):

        return redirect(
            url_for("admin_login")
        )

    connection = None
    cursor = None

    booking = None

    try:

        connection = get_db_connection()

        if connection is None:

            return (
                "Database connection failed",
                500
            )

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM bookings
            WHERE booking_id = %s
            """,
            (booking_id,)
        )

        booking = cursor.fetchone()

    except Exception as e:

        print(
            "Booking details error:",
            e
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

    if booking is None:

        return "Booking not found", 404

    return render_template(
        "booking_details.html",
        booking=booking
    )


# =========================================================
# CONFIRM BOOKING
# =========================================================
@app.route("/admin/booking/<booking_id>/confirm", methods=["POST"])
def confirm_booking(booking_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:
            return "Database connection failed.", 500

        cursor = connection.cursor(dictionary=True)

        # Check current booking status
        cursor.execute(
            """
            SELECT status
            FROM bookings
            WHERE booking_id = %s
            """,
            (booking_id,)
        )

        booking = cursor.fetchone()

        if not booking:
            return """
            <script>
                alert("Booking not found.");
                window.location.href = "/admin";
            </script>
            """

        # Do not confirm a cancelled booking
        if (
            booking["status"]
            and booking["status"].lower() == "cancelled"
        ):

            return """
            <script>
                alert(
                    "This booking has been cancelled by the customer \
and cannot be confirmed."
                );
                window.location.href =
                    "/admin/booking/%s";
            </script>
            """ % booking_id

        # Confirm booking
        cursor.execute(
            """
            UPDATE bookings
            SET status = 'Confirmed'
            WHERE booking_id = %s
            """,
            (booking_id,)
        )

        connection.commit()

        print(
            "Booking confirmed by admin:",
            booking_id
        )

    except Exception as e:

        print(
            "Error confirming booking:",
            e
        )

        if connection:
            connection.rollback()

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

    return redirect(
        url_for(
            "admin_booking_details",
            booking_id=booking_id
        )
    )

# =========================================================
# CANCEL BOOKING
# =========================================================

@app.route(
    "/admin/booking/<booking_id>/cancel",
    methods=["POST"]
)
def cancel_booking(booking_id):

    if not session.get(
        "admin_logged_in"
    ):

        return redirect(
            url_for("admin_login")
        )

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            return redirect(
                url_for("admin_dashboard")
            )

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE bookings
            SET status = 'Cancelled'
            WHERE booking_id = %s
            """,
            (booking_id,)
        )

        connection.commit()

    except Exception as e:

        print(
            "Cancel booking error:",
            e
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

    return redirect(
        url_for(
            "admin_booking_details",
            booking_id=booking_id
        )
    )


# =========================================================
# ADD NEW TREK
# =========================================================

@app.route(
    "/admin/add-trek",
    methods=["POST"]
)
def add_trek():

    if not session.get(
        "admin_logged_in"
    ):

        return redirect(
            url_for("admin_login")
        )

    trek_name = request.form.get(
        "trek_name",
        ""
    ).strip()

    location = request.form.get(
        "location",
        ""
    ).strip()

    difficulty = request.form.get(
        "difficulty",
        ""
    ).strip()

    duration = request.form.get(
        "duration",
        ""
    ).strip()

    distance = request.form.get(
        "distance",
        ""
    ).strip()

    elevation = request.form.get(
        "elevation",
        ""
    ).strip()

    price = request.form.get(
        "price",
        "0"
    ).strip()

    rating = request.form.get(
        "rating",
        "0"
    ).strip()

    mentor = request.form.get(
        "mentor",
        ""
    ).strip()

    short_description = request.form.get(
        "short_description",
        ""
    ).strip()

    description = request.form.get(
        "description",
        ""
    ).strip()

    image_file = request.files.get(
        "trek_image"
    )

    if not trek_name:

        return redirect(
            "/admin#treks"
        )

    if image_file is None:

        return redirect(
            "/admin#treks"
        )

    if image_file.filename == "":

        return redirect(
            "/admin#treks"
        )

    if not allowed_file(
        image_file.filename
    ):

        return redirect(
            "/admin#treks"
        )

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            return redirect(
                "/admin#treks"
            )

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT id
            FROM treks
            WHERE trek_name = %s
            """,
            (trek_name,)
        )

        existing = cursor.fetchone()

        if existing:

            print(
                f"Trek already exists: {trek_name}"
            )

            return redirect(
                "/admin#treks"
            )

    except Exception as e:

        print(
            "Duplicate trek check error:",
            e
        )

        return redirect(
            "/admin#treks"
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

    filename = secure_filename(
        image_file.filename
    )

    upload_folder = app.config[
        "UPLOAD_FOLDER"
    ]

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    image_path = os.path.join(
        upload_folder,
        filename
    )

    image_file.save(
        image_path
    )

    price_value = price_to_number(
        price
    )

    try:

        rating_value = float(
            rating
        )

    except:

        rating_value = 0

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            return redirect(
                "/admin#treks"
            )

        cursor = connection.cursor()

        query = """
        INSERT INTO treks (
            trek_name,
            location,
            image,
            difficulty,
            duration,
            distance,
            elevation,
            price,
            rating,
            mentor,
            short_description,
            description
        )
        VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
        """

        values = (

            trek_name,

            location,

            filename,

            difficulty,

            duration,

            distance,

            elevation,

            price_value,

            rating_value,

            mentor,

            short_description,

            description
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        # Update in-memory dictionary
        treks[trek_name] = {

            "name": trek_name,

            "location": location,

            "image": filename,

            "difficulty": difficulty,

            "duration": duration,

            "distance": distance,

            "elevation": elevation,

            "price": price_value,

            "rating": rating_value,

            "mentor": mentor,

            "short_description":
                short_description,

            "description":
                description
        }

        print(
            f"New trek added successfully: "
            f"{trek_name}"
        )

    except Exception as e:

        print(
            "Add trek database error:",
            e
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

    return redirect(
        "/admin#treks"
    )


# =========================================================
# DELETE TREK
# =========================================================

@app.route(
    "/admin/delete-trek/<path:trek_name>",
    methods=["POST"]
)
def delete_trek_route(trek_name):

    if not session.get(
        "admin_logged_in"
    ):

        return redirect(
            url_for("admin_login")
        )

    # Decode trek name from URL
    trek_name = unquote_plus(
        trek_name
    ).strip()

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            return redirect(
                "/admin#treks"
            )

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM treks
            WHERE trek_name = %s
            """,
            (trek_name,)
        )

        connection.commit()

        deleted_rows = cursor.rowcount

        if deleted_rows > 0:

            print(
                f"Trek deleted successfully: "
                f"{trek_name}"
            )

        else:

            print(
                f"Trek not found: "
                f"{trek_name}"
            )

        # Remove from memory
        for key in list(treks.keys()):

            if key.lower() == trek_name.lower():

                del treks[key]

                break

    except Exception as e:

        print(
            "Delete trek error:",
            e
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

    return redirect(
        "/admin#treks"
    )


# =========================================================
# EDIT TREK
# =========================================================

@app.route(
    "/admin/edit-trek/<path:trek_name>"
)
def edit_trek(trek_name):

    if not session.get(
        "admin_logged_in"
    ):

        return redirect(
            url_for("admin_login")
        )

    # Decode URL trek name
    trek_name = unquote_plus(
        trek_name
    ).strip()

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            return (
                "Database connection failed",
                500
            )

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM treks
            WHERE LOWER(trek_name) = LOWER(%s)
            """,
            (trek_name,)
        )

        trek = cursor.fetchone()

    except Exception as e:

        print(
            "Edit trek error:",
            e
        )

        return (
            "Database error while loading trek",
            500
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

    if not trek:

        return "Trek not found", 404

    trek["name"] = trek["trek_name"]

    return render_template(
        "edit_trek.html",
        trek=trek
    )


# =========================================================
# UPDATE TREK
# =========================================================

@app.route(
    "/admin/update-trek/<path:trek_name>",
    methods=["POST"]
)
def update_trek(trek_name):

    if not session.get(
        "admin_logged_in"
    ):

        return redirect(
            url_for("admin_login")
        )

    # Decode original trek name
    trek_name = unquote_plus(
        trek_name
    ).strip()

    trek_name_new = request.form.get(
        "trek_name",
        ""
    ).strip()

    location = request.form.get(
        "location",
        ""
    ).strip()

    difficulty = request.form.get(
        "difficulty",
        ""
    ).strip()

    duration = request.form.get(
        "duration",
        ""
    ).strip()

    distance = request.form.get(
        "distance",
        ""
    ).strip()

    elevation = request.form.get(
        "elevation",
        ""
    ).strip()

    price = request.form.get(
        "price",
        "0"
    ).strip()

    rating = request.form.get(
        "rating",
        "0"
    ).strip()

    mentor = request.form.get(
        "mentor",
        ""
    ).strip()

    short_description = request.form.get(
        "short_description",
        ""
    ).strip()

    description = request.form.get(
        "description",
        ""
    ).strip()

    image = request.files.get(
        "trek_image"
    )

    if not trek_name_new:

        return (
            "Trek name is required",
            400
        )

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            return (
                "Database connection failed",
                500
            )

        cursor = connection.cursor(
            dictionary=True
        )

        # -----------------------------------------
        # GET EXISTING TREK
        # -----------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM treks
            WHERE LOWER(trek_name) = LOWER(%s)
            """,
            (trek_name,)
        )

        existing_trek = cursor.fetchone()

        if not existing_trek:

            return (
                "Trek not found",
                404
            )

        # Get exact existing database name
        existing_name = existing_trek[
            "trek_name"
        ]

        # -----------------------------------------
        # CHECK DUPLICATE NEW NAME
        # -----------------------------------------

        if trek_name_new.lower() != existing_name.lower():

            cursor.execute(
                """
                SELECT id
                FROM treks
                WHERE LOWER(trek_name) = LOWER(%s)
                """,
                (trek_name_new,)
            )

            duplicate = cursor.fetchone()

            if duplicate:

                return (
                    "A trek with this name already exists",
                    400
                )

        # -----------------------------------------
        # KEEP OLD IMAGE BY DEFAULT
        # -----------------------------------------

        image_name = (
            existing_trek["image"]
            or ""
        )

        # -----------------------------------------
        # SAVE NEW IMAGE IF PROVIDED
        # -----------------------------------------

        if (
            image
            and image.filename
        ):

            if not allowed_file(
                image.filename
            ):

                return (
                    "Invalid image format",
                    400
                )

            filename = secure_filename(
                image.filename
            )

            image_folder = os.path.join(
                app.root_path,
                "static",
                "images"
            )

            os.makedirs(
                image_folder,
                exist_ok=True
            )

            image.save(
                os.path.join(
                    image_folder,
                    filename
                )
            )

            image_name = filename

        # -----------------------------------------
        # CONVERT NUMERIC VALUES
        # -----------------------------------------

        price_value = price_to_number(
            price
        )

        try:

            rating_value = float(
                rating
            )

        except:

            rating_value = 0

        # -----------------------------------------
        # UPDATE DATABASE
        # -----------------------------------------

        cursor.execute(
            """
            UPDATE treks
            SET
                trek_name = %s,
                location = %s,
                image = %s,
                difficulty = %s,
                duration = %s,
                distance = %s,
                elevation = %s,
                price = %s,
                rating = %s,
                mentor = %s,
                short_description = %s,
                description = %s
            WHERE LOWER(trek_name) = LOWER(%s)
            """,
            (
                trek_name_new,
                location,
                image_name,
                difficulty,
                duration,
                distance,
                elevation,
                price_value,
                rating_value,
                mentor,
                short_description,
                description,
                existing_name
            )
        )

        connection.commit()

        print(
            "Trek updated successfully:",
            trek_name_new
        )

    except Exception as e:

        print(
            "Update trek error:",
            e
        )

        if connection:

            connection.rollback()

        return (
            "Could not update trek",
            500
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

    # -----------------------------------------
    # RELOAD TREKS FROM MYSQL
    # -----------------------------------------

    load_treks_from_database()

    # -----------------------------------------
    # GO BACK TO ADMIN DASHBOARD
    # -----------------------------------------

    return redirect(
        url_for("admin_dashboard")
    )

# =========================================================
# UPDATE PAYMENT STATUS - PAID
# =========================================================

@app.route("/admin/payment/<booking_id>/paid", methods=["POST"])
def mark_payment_paid(booking_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()

        if connection is None:
            print("Could not connect to database while updating payment.")
            return redirect(url_for("admin_dashboard"))

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE bookings
            SET
                payment_status = 'Paid',
                payment_date = NOW()
            WHERE booking_id = %s
        """, (booking_id,))

        connection.commit()

        print("Payment marked as Paid:", booking_id)

    except Exception as e:
        print("Error marking payment as Paid:", e)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

    return redirect(url_for("admin_dashboard"))

# =========================================================
# UPDATE PAYMENT STATUS - REFUNDED
# =========================================================

@app.route("/admin/payment/<booking_id>/refunded", methods=["POST"])
def mark_payment_refunded(booking_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()

        if connection is None:
            print("Could not connect to database while updating payment.")
            return redirect(url_for("admin_dashboard"))

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE bookings
            SET
                payment_status = 'Refunded',
                payment_date = NOW()
            WHERE booking_id = %s
        """, (booking_id,))

        connection.commit()

        print("Payment marked as Refunded:", booking_id)

    except Exception as e:
        print("Error marking payment as Refunded:", e)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

    return redirect(url_for("admin_dashboard"))



@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    # Check required fields
    if not email or not password:
        return """
        <script>
            alert("Please enter your email and password.");
            window.history.back();
        </script>
        """

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:
            print("Could not connect to database during login.")

            return """
            <script>
                alert("Database connection failed. Please try again.");
                window.history.back();
            </script>
            """

        cursor = connection.cursor(dictionary=True)

        # Find customer by email
        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                phone,
                password_hash
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        # Check whether account exists
        if not user:

            return """
            <script>
                alert("No account found with this email. Please sign up first.");
                window.history.back();
            </script>
            """

        # Verify password
        if not check_password_hash(
            user["password_hash"],
            password
        ):

            return """
            <script>
                alert("Incorrect password. Please try again.");
                window.history.back();
            </script>
            """

        # Store customer information in Flask session
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        session["user_email"] = user["email"]

        print("Customer logged in:", user["email"])

        return """
        <script>
            alert("Login successful! Welcome to Trekora.");
            window.location.href = "/";
        </script>
        """

    except Exception as e:

        print("Login error:", e)

        return """
        <script>
            alert("Something went wrong while logging in.");
            window.history.back();
        </script>
        """

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "GET":
        return render_template("signup.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    phone = request.form.get("phone", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    # Check required fields
    if not name or not email or not password:
        return """
        <script>
            alert("Please fill in all required fields.");
            window.history.back();
        </script>
        """

    # Check password length
    if len(password) < 6:
        return """
        <script>
            alert("Password must contain at least 6 characters.");
            window.history.back();
        </script>
        """

    # Check password confirmation
    if password != confirm_password:
        return """
        <script>
            alert("Passwords do not match.");
            window.history.back();
        </script>
        """

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:
            print("Could not connect to database during signup.")

            return """
            <script>
                alert("Database connection failed. Please try again.");
                window.history.back();
            </script>
            """

        cursor = connection.cursor(dictionary=True)

        # Check whether email already exists
        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            return """
            <script>
                alert("An account with this email already exists. Please login.");
                window.location.href = "/login";
            </script>
            """

        # Create secure password hash
        password_hash = generate_password_hash(password)

        # Insert new user
        cursor.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                phone,
                password_hash
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                name,
                email,
                phone,
                password_hash
            )
        )

        connection.commit()

        print("New Trekora customer registered:", email)

        return """
        <script>
            alert("Account created successfully! Please login.");
            window.location.href = "/login";
        </script>
        """

    except Exception as e:

        print("Signup error:", e)

        if connection:
            connection.rollback()

        return """
        <script>
            alert("Something went wrong while creating your account.");
            window.history.back();
        </script>
        """

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()



@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route("/profile")
def profile():

    # User must be logged in
    if not session.get("user_id"):
        return redirect(
            url_for(
                "login",
                next="/profile"
            )
        )

    user_id = session.get("user_id")

    connection = None
    cursor = None

    try:
        connection = get_db_connection()

        if connection is None:
            return "Database connection failed.", 500

        cursor = connection.cursor(dictionary=True)

        # Get logged-in user's information
        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                phone,
                created_at
            FROM users
            WHERE id = %s
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if not user:
            session.clear()
            return redirect(url_for("login"))

        # Get only this user's bookings
        cursor.execute(
            """
            SELECT
                booking_id,
                trek_name,
                trek_date,
                people,
                experience,
                price_per_person,
                total_amount,
                status,
                payment_status,
                payment_method,
                payment_date,
                created_at
            FROM bookings
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,)
        )

        bookings = cursor.fetchall()

        return render_template(
            "profile.html",
            user=user,
            bookings=bookings
        )

    except Exception as e:

        print("Profile Error:", e)

        return "Something went wrong while loading your profile.", 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()



@app.route("/my-booking/<booking_id>/receipt")
def download_my_booking_receipt(booking_id):

    # Customer must be logged in
    if not session.get("user_id"):
        return redirect(
            url_for(
                "login",
                next=url_for(
                    "download_my_booking_receipt",
                    booking_id=booking_id
                )
            )
        )

    user_id = session.get("user_id")

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:
            return "Database connection failed.", 500

        cursor = connection.cursor(dictionary=True)

        # -------------------------------------------------
        # GET ONLY THE LOGGED-IN USER'S BOOKING
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT
                booking_id,
                trek_name,
                name,
                email,
                phone,
                trek_date,
                people,
                experience,
                price_per_person,
                total_amount,
                status,
                payment_status,
                payment_method,
                payment_date,
                created_at
            FROM bookings
            WHERE booking_id = %s
            AND user_id = %s
            """,
            (
                booking_id,
                user_id
            )
        )

        payment = cursor.fetchone()

        # -------------------------------------------------
        # BOOKING NOT FOUND
        # -------------------------------------------------

        if not payment:
            return """
            <script>
                alert(
                    "Booking not found or you do not have permission to access this receipt."
                );
                window.location.href = "/profile";
            </script>
            """

        # -------------------------------------------------
        # IMPORT REPORTLAB
        # -------------------------------------------------

        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors

        from reportlab.lib.styles import (
            getSampleStyleSheet,
            ParagraphStyle
        )

        from reportlab.lib.enums import TA_CENTER

        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle
        )

        from reportlab.lib.units import mm

        from io import BytesIO

        # -------------------------------------------------
        # CREATE PDF BUFFER
        # -------------------------------------------------

        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm
        )

        styles = getSampleStyleSheet()

        # -------------------------------------------------
        # PDF STYLES
        # -------------------------------------------------

        title_style = ParagraphStyle(
            "UserReceiptTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#28523d"),
            spaceAfter=5
        )

        subtitle_style = ParagraphStyle(
            "UserReceiptSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#6d7c73"),
            spaceAfter=18
        )

        section_style = ParagraphStyle(
            "UserReceiptSection",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#28523d"),
            spaceBefore=8,
            spaceAfter=8
        )

        normal_style = ParagraphStyle(
            "UserReceiptNormal",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#34463c")
        )

        # -------------------------------------------------
        # HELPER FUNCTION
        # -------------------------------------------------

        def safe_value(
            value,
            default="Not Available"
        ):

            if value is None:
                return default

            if str(value).strip() == "":
                return default

            return str(value)

        # -------------------------------------------------
        # FORMAT VALUES
        # -------------------------------------------------

        payment_status = safe_value(
            payment.get("payment_status"),
            "Pending"
        )

        payment_method = safe_value(
            payment.get("payment_method"),
            "Not Selected"
        )

        booking_status = safe_value(
            payment.get("status"),
            "Pending"
        )

        experience = safe_value(
            payment.get("experience"),
            "Not Specified"
        )

        # -------------------------------------------------
        # TREK DATE
        # -------------------------------------------------

        trek_date = payment.get("trek_date")

        if trek_date:
            trek_date = trek_date.strftime(
                "%d %B %Y"
            )
        else:
            trek_date = "Not Available"

        # -------------------------------------------------
        # PAYMENT DATE
        # -------------------------------------------------

        payment_date = payment.get("payment_date")

        if payment_date:
            payment_date = payment_date.strftime(
                "%d %B %Y, %I:%M %p"
            )
        else:
            payment_date = "Not Available"

        # -------------------------------------------------
        # BOOKING CREATED DATE
        # -------------------------------------------------

        created_at = payment.get("created_at")

        if created_at:
            created_at = created_at.strftime(
                "%d %B %Y, %I:%M %p"
            )
        else:
            created_at = "Not Available"

        # -------------------------------------------------
        # TOTAL AMOUNT
        # -------------------------------------------------

        try:
            total_amount = float(
                payment.get("total_amount") or 0
            )
        except:
            total_amount = 0

        # -------------------------------------------------
        # PRICE PER PERSON
        # -------------------------------------------------

        try:
            price_per_person = float(
                payment.get("price_per_person") or 0
            )
        except:
            price_per_person = 0

        # -------------------------------------------------
        # PDF STORY
        # -------------------------------------------------

        story = []

        # -------------------------------------------------
        # TREKORA TITLE
        # -------------------------------------------------

        story.append(
            Paragraph(
                "TREKORA",
                title_style
            )
        )

        story.append(
            Paragraph(
                "Trekking Management Platform",
                subtitle_style
            )
        )

        # -------------------------------------------------
        # RECEIPT HEADER
        # -------------------------------------------------

        receipt_header = Table(
            [
                [
                    Paragraph(
                        "<b>PAYMENT RECEIPT</b>",
                        normal_style
                    ),

                    Paragraph(
                        "<b>Booking ID</b><br/>"
                        + safe_value(
                            payment.get("booking_id")
                        ),
                        normal_style
                    )
                ]
            ],
            colWidths=[
                90 * mm,
                70 * mm
            ]
        )

        receipt_header.setStyle(
            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#e8f3ec")
                ),

                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    colors.HexColor("#c7dbce")
                ),

                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#d5e4da")
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    9
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    9
                )

            ])
        )

        story.append(
            receipt_header
        )

        story.append(
            Spacer(1, 12)
        )

        # -------------------------------------------------
        # CUSTOMER INFORMATION
        # -------------------------------------------------

        story.append(
            Paragraph(
                "Customer Information",
                section_style
            )
        )

        customer_data = [

            [
                Paragraph(
                    "<b>Name</b>",
                    normal_style
                ),

                Paragraph(
                    safe_value(
                        payment.get("name")
                    ),
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>Email</b>",
                    normal_style
                ),

                Paragraph(
                    safe_value(
                        payment.get("email")
                    ),
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>Phone</b>",
                    normal_style
                ),

                Paragraph(
                    safe_value(
                        payment.get("phone")
                    ),
                    normal_style
                )
            ]

        ]

        customer_table = Table(
            customer_data,
            colWidths=[
                45 * mm,
                115 * mm
            ]
        )

        customer_table.setStyle(
            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#f3f7f4")
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#dce6df")
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )

            ])
        )

        story.append(
            customer_table
        )

        # -------------------------------------------------
        # TREK INFORMATION
        # -------------------------------------------------

        story.append(
            Paragraph(
                "Trek Information",
                section_style
            )
        )

        trek_data = [

            [
                Paragraph(
                    "<b>Trek</b>",
                    normal_style
                ),

                Paragraph(
                    safe_value(
                        payment.get("trek_name")
                    ),
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>Trek Date</b>",
                    normal_style
                ),

                Paragraph(
                    trek_date,
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>People</b>",
                    normal_style
                ),

                Paragraph(
                    safe_value(
                        payment.get("people")
                    ),
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>Experience</b>",
                    normal_style
                ),

                Paragraph(
                    experience,
                    normal_style
                )
            ]

        ]

        trek_table = Table(
            trek_data,
            colWidths=[
                45 * mm,
                115 * mm
            ]
        )

        trek_table.setStyle(
            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#f3f7f4")
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#dce6df")
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )

            ])
        )

        story.append(
            trek_table
        )

        # -------------------------------------------------
        # PAYMENT INFORMATION
        # -------------------------------------------------

        story.append(
            Paragraph(
                "Payment Information",
                section_style
            )
        )

        payment_data = [

            [
                Paragraph(
                    "<b>Total Amount</b>",
                    normal_style
                ),

                Paragraph(
                    f"<b>Rs. {total_amount:.2f}</b>",
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>Price Per Person</b>",
                    normal_style
                ),

                Paragraph(
                    f"Rs. {price_per_person:.2f}",
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>Payment Method</b>",
                    normal_style
                ),

                Paragraph(
                    payment_method,
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>Payment Status</b>",
                    normal_style
                ),

                Paragraph(
                    payment_status,
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>Payment Date</b>",
                    normal_style
                ),

                Paragraph(
                    payment_date,
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>Booking Status</b>",
                    normal_style
                ),

                Paragraph(
                    booking_status,
                    normal_style
                )
            ]

        ]

        payment_table = Table(
            payment_data,
            colWidths=[
                55 * mm,
                105 * mm
            ]
        )

        payment_table.setStyle(
            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#f3f7f4")
                ),

                (
                    "BACKGROUND",
                    (1, 0),
                    (1, 0),
                    colors.HexColor("#e5f2e9")
                ),

                (
                    "TEXTCOLOR",
                    (1, 0),
                    (1, 0),
                    colors.HexColor("#246c49")
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#dce6df")
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )

            ])
        )

        story.append(
            payment_table
        )

        # -------------------------------------------------
        # FOOTER
        # -------------------------------------------------

        story.append(
            Spacer(1, 18)
        )

        story.append(
            Paragraph(
                "This receipt was generated by Trekora.",
                subtitle_style
            )
        )

        story.append(
            Paragraph(
                f"Booking created: {created_at}",
                subtitle_style
            )
        )

        # -------------------------------------------------
        # BUILD PDF
        # -------------------------------------------------

        document.build(
            story
        )

        buffer.seek(0)

        # -------------------------------------------------
        # SEND PDF TO USER
        # -------------------------------------------------

        from flask import send_file

        return send_file(
            buffer,
            as_attachment=True,
            download_name=(
                f"Trekora_Receipt_"
                f"{booking_id}.pdf"
            ),
            mimetype="application/pdf"
        )

    except Exception as e:

        print(
            "Customer Receipt Error:",
            repr(e)
        )

        return """
        <script>
            alert(
                "Unable to generate your receipt."
            );
            window.history.back();
        </script>
        """

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


@app.route("/my-booking/<booking_id>")
def my_booking_details(booking_id):

    # Customer must be logged in
    if not session.get("user_id"):
        return redirect(
            url_for(
                "login",
                next=url_for(
                    "my_booking_details",
                    booking_id=booking_id
                )
            )
        )

    user_id = session.get("user_id")

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:
            return "Database connection failed.", 500

        cursor = connection.cursor(dictionary=True)

        # Only allow the logged-in customer
        # to view their own booking
        cursor.execute(
            """
            SELECT
                booking_id,
                trek_name,
                name,
                email,
                phone,
                trek_date,
                people,
                experience,
                emergency_name,
                emergency_phone,
                price_per_person,
                total_amount,
                status,
                payment_status,
                payment_method,
                payment_date,
                created_at
            FROM bookings
            WHERE booking_id = %s
            AND user_id = %s
            """,
            (
                booking_id,
                user_id
            )
        )

        booking = cursor.fetchone()

        if not booking:
            return """
            <!DOCTYPE html>
            <html>
            <head>

                <title>Booking Not Found | Trekora</title>

                <style>

                    body {
                        font-family: Arial, sans-serif;
                        background: #f3f7f4;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        min-height: 100vh;
                        margin: 0;
                    }

                    .message {
                        background: white;
                        padding: 40px;
                        border-radius: 16px;
                        text-align: center;
                        box-shadow:
                            0 10px 35px
                            rgba(0, 0, 0, 0.10);
                    }

                    h2 {
                        color: #294238;
                    }

                    p {
                        color: #7b8982;
                    }

                    a {
                        display: inline-block;
                        margin-top: 15px;
                        padding: 10px 18px;
                        background: #294238;
                        color: white;
                        text-decoration: none;
                        border-radius: 8px;
                    }

                </style>

            </head>

            <body>

                <div class="message">

                    <h2>
                        Booking Not Found
                    </h2>

                    <p>
                        This booking does not exist or does not
                        belong to your account.
                    </p>

                    <a href="/profile">
                        Back to Profile
                    </a>

                </div>

            </body>
            </html>
            """, 404

        return render_template(
            "my_booking_details.html",
            booking=booking
        )

    except Exception as e:

        print(
            "Customer Booking Details Error:",
            e
        )

        return (
            "Something went wrong while loading your booking.",
            500
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


            
@app.route("/my-booking/<booking_id>/cancel", methods=["POST"])
def cancel_my_booking(booking_id):

    # Customer must be logged in
    if not session.get("user_id"):
        return redirect(
            url_for(
                "login",
                next=url_for(
                    "my_booking_details",
                    booking_id=booking_id
                )
            )
        )

    user_id = session.get("user_id")

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:
            return "Database connection failed.", 500

        cursor = connection.cursor(dictionary=True)

        # Check that this booking belongs to the
        # currently logged-in customer
        cursor.execute(
            """
            SELECT
                booking_id,
                status,
                payment_status
            FROM bookings
            WHERE booking_id = %s
            AND user_id = %s
            """,
            (
                booking_id,
                user_id
            )
        )

        booking = cursor.fetchone()

        if not booking:
            return """
            <script>
                alert("Booking not found.");
                window.location.href = "/profile";
            </script>
            """, 404

        current_status = (
            booking["status"] or "Pending"
        ).lower()

        # Already cancelled
        if current_status == "cancelled":

            return """
            <script>
                alert("This booking is already cancelled.");
                window.location.href = "/profile";
            </script>
            """

        # Don't allow cancellation after payment refund
        if (
            booking["payment_status"]
            and booking["payment_status"].lower() == "refunded"
        ):

            return """
            <script>
                alert("This booking has already been refunded.");
                window.location.href = "/profile";
            </script>
            """

        # Cancel booking
        cursor.execute(
            """
            UPDATE bookings
            SET status = 'Cancelled'
            WHERE booking_id = %s
            AND user_id = %s
            """,
            (
                booking_id,
                user_id
            )
        )

        connection.commit()

        print(
            "Customer cancelled booking:",
            booking_id
        )

        return redirect(
            url_for(
                "my_booking_details",
                booking_id=booking_id
            )
        )

    except Exception as e:

        print(
            "Customer cancellation error:",
            e
        )

        if connection:
            connection.rollback()

        return """
        <script>
            alert("Unable to cancel the booking. Please try again.");
            window.history.back();
        </script>
        """

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


@app.route("/admin/payment/<booking_id>/receipt")
def download_payment_receipt(booking_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    connection = None
    cursor = None

    try:

        # -------------------------------------------------
        # GET PAYMENT DATA
        # -------------------------------------------------

        connection = get_db_connection()

        if connection is None:
            return "Database connection failed.", 500

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                booking_id,
                trek_name,
                name,
                email,
                phone,
                trek_date,
                people,
                experience,
                price_per_person,
                total_amount,
                status,
                payment_status,
                payment_method,
                payment_date,
                created_at
            FROM bookings
            WHERE booking_id = %s
        """, (booking_id,))

        payment = cursor.fetchone()

        if not payment:
            return """
            <script>
                alert("Payment record not found.");
                window.location.href = "/admin#payments";
            </script>
            """

        # -------------------------------------------------
        # IMPORT REPORTLAB
        # -------------------------------------------------

        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors

        from reportlab.lib.styles import (
            getSampleStyleSheet,
            ParagraphStyle
        )

        from reportlab.lib.enums import (
            TA_CENTER
        )

        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle
        )

        from reportlab.lib.units import mm

        from io import BytesIO

        # -------------------------------------------------
        # CREATE PDF BUFFER
        # -------------------------------------------------

        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm
        )

        styles = getSampleStyleSheet()

        # -------------------------------------------------
        # PDF STYLES
        # -------------------------------------------------

        title_style = ParagraphStyle(
            "ReceiptTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#28523d"),
            spaceAfter=5
        )

        subtitle_style = ParagraphStyle(
            "ReceiptSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#6d7c73"),
            spaceAfter=18
        )

        section_style = ParagraphStyle(
            "SectionTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#28523d"),
            spaceBefore=8,
            spaceAfter=8
        )

        normal_style = ParagraphStyle(
            "ReceiptNormal",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#34463c")
        )

        # -------------------------------------------------
        # HELPER FUNCTION
        # -------------------------------------------------

        def safe_value(
            value,
            default="Not Available"
        ):

            if value is None:
                return default

            if str(value).strip() == "":
                return default

            return str(value)

        # -------------------------------------------------
        # FORMAT PAYMENT VALUES
        # -------------------------------------------------

        payment_status = safe_value(
            payment.get("payment_status"),
            "Pending"
        )

        payment_method = safe_value(
            payment.get("payment_method"),
            "Not Selected"
        )

        booking_status = safe_value(
            payment.get("status"),
            "Pending"
        )

        experience = safe_value(
            payment.get("experience"),
            "Not Specified"
        )

        # -------------------------------------------------
        # TREK DATE
        # -------------------------------------------------

        trek_date = payment.get("trek_date")

        if trek_date:

            trek_date = trek_date.strftime(
                "%d %B %Y"
            )

        else:

            trek_date = "Not Available"

        # -------------------------------------------------
        # PAYMENT DATE
        # -------------------------------------------------

        payment_date = payment.get("payment_date")

        if payment_date:

            payment_date = payment_date.strftime(
                "%d %B %Y, %I:%M %p"
            )

        else:

            payment_date = "Not Available"

        # -------------------------------------------------
        # BOOKING CREATED DATE
        # -------------------------------------------------

        created_at = payment.get("created_at")

        if created_at:

            created_at = created_at.strftime(
                "%d %B %Y, %I:%M %p"
            )

        else:

            created_at = "Not Available"

        # -------------------------------------------------
        # TOTAL AMOUNT
        # -------------------------------------------------

        try:

            total_amount = float(
                payment.get("total_amount") or 0
            )

        except:

            total_amount = 0

        # -------------------------------------------------
        # PRICE PER PERSON
        # -------------------------------------------------

        try:

            price_per_person = float(
                payment.get("price_per_person") or 0
            )

        except:

            price_per_person = 0

        # -------------------------------------------------
        # PDF STORY
        # -------------------------------------------------

        story = []

        # -------------------------------------------------
        # TREKORA TITLE
        # -------------------------------------------------

        story.append(
            Paragraph(
                "TREKORA",
                title_style
            )
        )

        story.append(
            Paragraph(
                "Trekking Management Platform",
                subtitle_style
            )
        )

        # -------------------------------------------------
        # RECEIPT HEADER
        # -------------------------------------------------

        receipt_header = Table(
            [
                [
                    Paragraph(
                        "<b>PAYMENT RECEIPT</b>",
                        normal_style
                    ),

                    Paragraph(
                        "<b>Booking ID</b><br/>"
                        + safe_value(
                            payment.get("booking_id")
                        ),
                        normal_style
                    )
                ]
            ],
            colWidths=[
                90 * mm,
                70 * mm
            ]
        )

        receipt_header.setStyle(
            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#e8f3ec")
                ),

                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    colors.HexColor("#c7dbce")
                ),

                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#d5e4da")
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    9
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    9
                )

            ])
        )

        story.append(
            receipt_header
        )

        story.append(
            Spacer(1, 12)
        )

        # -------------------------------------------------
        # CUSTOMER INFORMATION
        # -------------------------------------------------

        story.append(
            Paragraph(
                "Customer Information",
                section_style
            )
        )

        customer_data = [

            [
                Paragraph(
                    "<b>Name</b>",
                    normal_style
                ),

                Paragraph(
                    safe_value(
                        payment.get("name")
                    ),
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>Email</b>",
                    normal_style
                ),

                Paragraph(
                    safe_value(
                        payment.get("email")
                    ),
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>Phone</b>",
                    normal_style
                ),

                Paragraph(
                    safe_value(
                        payment.get("phone")
                    ),
                    normal_style
                )
            ]

        ]

        customer_table = Table(
            customer_data,
            colWidths=[
                45 * mm,
                115 * mm
            ]
        )

        customer_table.setStyle(
            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#f3f7f4")
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#dce6df")
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )

            ])
        )

        story.append(
            customer_table
        )

        # -------------------------------------------------
        # TREK INFORMATION
        # -------------------------------------------------

        story.append(
            Paragraph(
                "Trek Information",
                section_style
            )
        )

        trek_data = [

            [
                Paragraph(
                    "<b>Trek</b>",
                    normal_style
                ),

                Paragraph(
                    safe_value(
                        payment.get("trek_name")
                    ),
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>Trek Date</b>",
                    normal_style
                ),

                Paragraph(
                    trek_date,
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>People</b>",
                    normal_style
                ),

                Paragraph(
                    safe_value(
                        payment.get("people")
                    ),
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>Experience</b>",
                    normal_style
                ),

                Paragraph(
                    experience,
                    normal_style
                )
            ]

        ]

        trek_table = Table(
            trek_data,
            colWidths=[
                45 * mm,
                115 * mm
            ]
        )

        trek_table.setStyle(
            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#f3f7f4")
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#dce6df")
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )

            ])
        )

        story.append(
            trek_table
        )

        # -------------------------------------------------
        # PAYMENT INFORMATION
        # -------------------------------------------------

        story.append(
            Paragraph(
                "Payment Information",
                section_style
            )
        )

        payment_data = [

            [
                Paragraph(
                    "<b>Total Amount</b>",
                    normal_style
                ),

                Paragraph(
                    f"<b>Rs. {total_amount:.2f}</b>",
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>Price Per Person</b>",
                    normal_style
                ),

                Paragraph(
                    f"Rs. {price_per_person:.2f}",
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>Payment Method</b>",
                    normal_style
                ),

                Paragraph(
                    payment_method,
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>Payment Status</b>",
                    normal_style
                ),

                Paragraph(
                    payment_status,
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>Payment Date</b>",
                    normal_style
                ),

                Paragraph(
                    payment_date,
                    normal_style
                )
            ],

            [
                Paragraph(
                    "<b>Booking Status</b>",
                    normal_style
                ),

                Paragraph(
                    booking_status,
                    normal_style
                )
            ]

        ]

        payment_table = Table(
            payment_data,
            colWidths=[
                55 * mm,
                105 * mm
            ]
        )

        payment_table.setStyle(
            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#f3f7f4")
                ),

                (
                    "BACKGROUND",
                    (1, 0),
                    (1, 0),
                    colors.HexColor("#e5f2e9")
                ),

                (
                    "TEXTCOLOR",
                    (1, 0),
                    (1, 0),
                    colors.HexColor("#246c49")
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#dce6df")
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )

            ])
        )

        story.append(
            payment_table
        )

        # -------------------------------------------------
        # FOOTER INFORMATION
        # -------------------------------------------------

        story.append(
            Spacer(1, 18)
        )

        story.append(
            Paragraph(
                "This receipt was generated by Trekora.",
                subtitle_style
            )
        )

        story.append(
            Paragraph(
                f"Booking created: {created_at}",
                subtitle_style
            )
        )

        # -------------------------------------------------
        # BUILD PDF
        # -------------------------------------------------

        document.build(
            story
        )

        buffer.seek(0)

        # -------------------------------------------------
        # SEND PDF
        # -------------------------------------------------

        from flask import send_file

        return send_file(
            buffer,
            as_attachment=True,
            download_name=(
                f"Trekora_Receipt_"
                f"{booking_id}.pdf"
            ),
            mimetype="application/pdf"
        )

    except Exception as e:

        print(
            "Payment Receipt Error:",
            repr(e)
        )

        return """
        <script>
            alert(
                "Unable to generate payment receipt."
            );
            window.history.back();
        </script>
        """

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

# =========================================================
# UPDATE BOOKING SETTINGS
# =========================================================

@app.route(
    "/admin/update-booking-setting",
    methods=["POST"]
)
def update_booking_setting():

    if not session.get("admin_logged_in"):
        return {
            "success": False,
            "message": "Unauthorized"
        }, 401

    data = request.get_json()

    if not data:
        return {
            "success": False,
            "message": "No data received"
        }, 400

    setting_name = data.get(
        "setting_name"
    )

    setting_value = data.get(
        "setting_value"
    )

    if setting_name not in [
        "allow_bookings",
        "auto_confirmation",
        "max_travellers"
    ]:

        return {
            "success": False,
            "message": "Invalid setting"
        }, 400
    print(
    "Updating setting:",
    setting_name,
    "=",
    setting_value
)
    success = update_admin_setting(
        setting_name,
        str(setting_value)
    )

    if not success:

        return {
            "success": False,
            "message": "Could not update setting"
        }, 500

    return {
        "success": True,
        "message": "Setting updated successfully"
    }

@app.route(
    "/admin/update-booking-status/<booking_id>",
    methods=["POST"]
)
def update_booking_status(booking_id):

    if not session.get("admin_logged_in"):
        return {
            "success": False,
            "message": "Unauthorized"
        }, 401

    new_status = request.form.get(
        "status",
        ""
    ).strip()

    allowed_statuses = [
        "Pending",
        "Confirmed",
        "Cancelled"
    ]

    if new_status not in allowed_statuses:
        return {
            "success": False,
            "message": "Invalid booking status"
        }, 400

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:
            return {
                "success": False,
                "message": "Database connection failed"
            }, 500

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE bookings
            SET status = %s
            WHERE booking_id = %s
            """,
            (
                new_status,
                booking_id
            )
        )

        if cursor.rowcount == 0:

            return {
                "success": False,
                "message": "Booking not found"
            }, 404

        connection.commit()

        print(
            "Booking status updated:",
            booking_id,
            "->",
            new_status
        )

        return redirect(
            url_for(
                "admin_booking_details",
                booking_id=booking_id
            )
        )

    except Exception as e:

        print(
            "Update Booking Status Error:",
            e
        )

        if connection:
            connection.rollback()

        return {
            "success": False,
            "message": "Unable to update booking status"
        }, 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.route(
    "/admin/update-notification-setting",
    methods=["POST"]
)
def update_notification_setting():

    if not session.get("admin_logged_in"):

        return {
            "success": False,
            "message": "Unauthorized"
        }, 401


    data = request.get_json()

    if not data:

        return {
            "success": False,
            "message": "No data received"
        }, 400


    setting_name = data.get(
        "setting_name"
    )

    setting_value = data.get(
        "setting_value"
    )


    allowed_settings = [
        "booking_notifications",
        "payment_notifications",
        "cancellation_notifications"
    ]


    if setting_name not in allowed_settings:

        return {
            "success": False,
            "message": "Invalid notification setting"
        }, 400


    if isinstance(
        setting_value,
        bool
    ):

        setting_value = (
            "true"
            if setting_value
            else "false"
        )


    print(
        "Updating notification setting:",
        setting_name,
        "=",
        setting_value
    )


    success = update_admin_setting(
        setting_name,
        str(setting_value)
    )


    if not success:

        return {
            "success": False,
            "message":
                "Could not update notification setting"
        }, 500


    return {
        "success": True,
        "message":
            "Notification setting updated successfully"
    }

@app.route(
    "/admin/notifications",
    methods=["GET"]
)
def admin_notifications():

    if not session.get("admin_logged_in"):

        return {
            "success": False,
            "message": "Unauthorized"
        }, 401


    notifications = get_notifications(
        None,
        20
    )


    unread_count = 0

    for notification in notifications:

        if not notification["is_read"]:
            unread_count += 1


    return {
        "success": True,
        "unread_count": unread_count
    }

@app.route(
    "/admin/notifications/list",
    methods=["GET"]
)
def admin_notification_list():

    if not session.get("admin_logged_in"):

        return {
            "success": False,
            "message": "Unauthorized"
        }, 401


    notifications = get_notifications(
        None,
        20
    )


    notification_data = []


    for notification in notifications:

        notification_data.append({

            "id": notification["id"],

            "type": notification["type"],

            "title": notification["title"],

            "message": notification["message"],

            "booking_id":
                notification["booking_id"],

            "is_read":
                bool(notification["is_read"]),

            "created_at":
                str(notification["created_at"])
        })


    return {

        "success": True,

        "notifications":
            notification_data
    }


# =====================================================
# AI TREK RECOMMENDATION API
# =====================================================

@app.route(
    "/api/ai-recommend",
    methods=["POST"]
)
def ai_recommend():

    try:

        data = request.get_json()

        if not data:
            return {
                "success": False,
                "message": "No data received."
            }, 400


        difficulty_score = int(
            data.get(
                "difficulty_score",
                2
            )
        )

        days = int(
            data.get(
                "days",
                1
            )
        )

        distance_km = float(
            data.get(
                "distance_km",
                8
            )
        )

        altitude_m = float(
            data.get(
                "altitude_m",
                1500
            )
        )

        price = float(
            data.get(
                "price",
                1000
            )
        )

        rating = float(
            data.get(
                "rating",
                4.5
            )
        )


        recommendations = recommend_treks(
            difficulty_score,
            days,
            distance_km,
            altitude_m,
            price,
            rating
        )


        return {
            "success": True,
            "recommendations":
                recommendations
        }


    except Exception as e:

        print(
            "AI Recommendation Error:",
            e
        )

        return {
            "success": False,
            "message":
                "Unable to generate recommendations."
        }, 500
    
@app.route("/ai-trek-finder")
def ai_trek_finder():

    return render_template(
        "ai_trek_finder.html"
    )
# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    # Create default records only if
    # database is completely empty.

    save_default_treks_to_database()

    # Load database records.

    load_treks_from_database()

    app.run(
        debug=True
    )

    