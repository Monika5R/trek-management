import mysql.connector
from mysql.connector import Error


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db_connection():

    try:

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root@123",
            database="trekora"
        )

        return connection

    except Error as e:

        print(
            "MySQL Connection Error:",
            e
        )

        return None


# ============================================================
# SAVE BOOKING
# ============================================================

def save_booking(
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
    payment_method
):

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            return False


        # ====================================================
        # GET AUTOMATIC BOOKING CONFIRMATION SETTING
        # ====================================================

        setting_cursor = connection.cursor(
            dictionary=True
        )

        setting_query = """
        SELECT setting_value
        FROM admin_settings
        WHERE setting_name = %s
        """

        setting_cursor.execute(
            setting_query,
            ("auto_confirmation",)
        )

        setting = setting_cursor.fetchone()

        setting_cursor.close()


        # ====================================================
        # DETERMINE BOOKING STATUS
        # ====================================================

        if setting:

            auto_confirmation = setting[
                "setting_value"
            ]

        else:

            auto_confirmation = "false"


        if str(
            auto_confirmation
        ).lower() == "true":

            booking_status = "Confirmed"

        else:

            booking_status = "Pending"


        print(
            "Automatic Booking Confirmation:",
            auto_confirmation
        )

        print(
            "New Booking Status:",
            booking_status
        )


        # ====================================================
        # CREATE BOOKING CURSOR
        # ====================================================

        cursor = connection.cursor()


        # ====================================================
        # INSERT BOOKING
        # ====================================================

        query = """
        INSERT INTO bookings (
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
            payment_method
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """


        values = (
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

            # Dynamic booking status
            booking_status,

            # Payment remains Pending
            "Pending",

            payment_method
        )


        cursor.execute(
            query,
            values
        )

        connection.commit()


        print(
            "Booking saved successfully!"
        )

        print(
            "Booking ID:",
            booking_id
        )

        print(
            "Booking Status:",
            booking_status
        )

        return True


    except Error as e:

        print(
            "Booking Save Error:",
            e
        )

        if connection:

            connection.rollback()

        return False


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# ============================================================
# DELETE TREK
# ============================================================

def delete_trek(trek_name):

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            return False

        cursor = connection.cursor()

        query = """
        DELETE FROM treks
        WHERE name = %s
        """

        cursor.execute(
            query,
            (trek_name,)
        )

        connection.commit()

        if cursor.rowcount > 0:

            print(
                "Trek deleted successfully:",
                trek_name
            )

            return True

        print(
            "Trek not found:",
            trek_name
        )

        return False


    except Error as e:

        print(
            "Trek Delete Error:",
            e
        )

        return False


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# ============================================================
# GET ALL TREKS
# ============================================================

def get_all_treks():

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            print(
                "Could not connect to database "
                "while loading treks."
            )

            return []

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
        SELECT
            id,
            name,
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
        """

        cursor.execute(query)

        treks = cursor.fetchall()

        print(
            "Treks loaded from database:",
            len(treks)
        )

        return treks


    except Error as e:

        print(
            "Get Treks Error:",
            e
        )

        return []


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# ============================================================
# GET ALL MENTORS
# ============================================================

def get_all_mentors():

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            print(
                "Could not connect to database "
                "while loading mentors."
            )

            return []

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
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
        ORDER BY id ASC
        """

        cursor.execute(query)

        mentors = cursor.fetchall()

        print(
            "Mentors loaded from database:",
            len(mentors)
        )

        return mentors


    except Error as e:

        print(
            "Get Mentors Error:",
            e
        )

        return []


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# ============================================================
# GET ALL USERS
# ============================================================

def get_all_users():

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            print(
                "Could not connect to database "
                "while loading users."
            )

            return []

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
        SELECT
            id,
            name,
            email,
            phone,
            created_at
        FROM users
        ORDER BY id DESC
        """

        cursor.execute(query)

        users = cursor.fetchall()

        print(
            "Users loaded from database:",
            len(users)
        )

        return users


    except Error as e:

        print(
            "Get Users Error:",
            e
        )

        return []


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# ============================================================
# GET ADMIN SETTING
# ============================================================

def get_admin_setting(
    setting_name,
    default=None
):

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            return default

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
        SELECT setting_value
        FROM admin_settings
        WHERE setting_name = %s
        """

        cursor.execute(
            query,
            (setting_name,)
        )

        setting = cursor.fetchone()

        if setting:

            return setting[
                "setting_value"
            ]

        return default


    except Error as e:

        print(
            "Get Admin Setting Error:",
            e
        )

        return default


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# ============================================================
# UPDATE ADMIN SETTING
# ============================================================

def update_admin_setting(
    setting_name,
    setting_value
):

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:

            return False

        cursor = connection.cursor()

        query = """
        INSERT INTO admin_settings (
            setting_name,
            setting_value
        )
        VALUES (
            %s,
            %s
        )

        ON DUPLICATE KEY UPDATE
            setting_value = VALUES(setting_value)
        """

        cursor.execute(
            query,
            (
                setting_name,
                setting_value
            )
        )

        connection.commit()

        return True


    except Error as e:

        print(
            "Update Admin Setting Error:",
            e
        )

        if connection:

            connection.rollback()

        return False


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()

def create_notification(
    user_id,
    notification_type,
    title,
    message,
    booking_id=None
):
    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        query = """
        INSERT INTO notifications (
            user_id,
            type,
            title,
            message,
            booking_id,
            is_read
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            FALSE
        )
        """

        values = (
            user_id,
            notification_type,
            title,
            message,
            booking_id
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        print(
            "Notification created:",
            title
        )

        return True

    except Error as e:

        print(
            "Create Notification Error:",
            e
        )

        if connection:
            connection.rollback()

        return False

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def get_notifications(
    user_id=None,
    limit=20
):
    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        if connection is None:
            return []

        cursor = connection.cursor(
            dictionary=True
        )

        if user_id is not None:

            query = """
            SELECT
                id,
                user_id,
                type,
                title,
                message,
                booking_id,
                is_read,
                created_at
            FROM notifications
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT %s
            """

            cursor.execute(
                query,
                (
                    user_id,
                    limit
                )
            )

        else:

            query = """
            SELECT
                id,
                user_id,
                type,
                title,
                message,
                booking_id,
                is_read,
                created_at
            FROM notifications
            ORDER BY created_at DESC
            LIMIT %s
            """

            cursor.execute(
                query,
                (limit,)
            )

        notifications = cursor.fetchall()

        return notifications

    except Error as e:

        print(
            "Get Notifications Error:",
            e
        )

        return []

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()