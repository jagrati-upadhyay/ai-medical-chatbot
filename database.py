import sqlite3
import uuid


DATABASE_NAME = "chat_history.db"


# --------------------------------
# Create / Update Database
# --------------------------------

def init_db():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            symptoms TEXT,
            duration TEXT,
            category TEXT,
            confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # --------------------------------
    # Add missing columns to old database
    # --------------------------------

    cursor.execute("PRAGMA table_info(conversations)")

    existing_columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    new_columns = {
        "symptoms": "TEXT",
        "duration": "TEXT",
        "category": "TEXT",
        "confidence": "REAL"
    }

    for column_name, column_type in new_columns.items():

        if column_name not in existing_columns:

            cursor.execute(
                f"""
                ALTER TABLE conversations
                ADD COLUMN {column_name} {column_type}
                """
            )

    connection.commit()

    connection.close()


# --------------------------------
# Create New Session
# --------------------------------

def create_session():

    return str(uuid.uuid4())


# --------------------------------
# Save Message
# --------------------------------

def save_message(
    session_id,
    role,
    message,
    symptoms=None,
    duration=None,
    category=None,
    confidence=None
):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO conversations
        (
            session_id,
            role,
            message,
            symptoms,
            duration,
            category,
            confidence
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            role,
            message,
            symptoms,
            duration,
            category,
            confidence
        )
    )

    connection.commit()

    connection.close()


# --------------------------------
# Get All Chat Sessions
# --------------------------------

def get_sessions():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            session_id,
            MIN(created_at) AS created_at
        FROM conversations
        GROUP BY session_id
        ORDER BY created_at DESC
    """)

    sessions = cursor.fetchall()

    connection.close()

    return sessions


# --------------------------------
# Get Specific Session History
# --------------------------------

def get_session_history(session_id):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            role,
            message,
            symptoms,
            duration,
            category,
            confidence
        FROM conversations
        WHERE session_id = ?
        ORDER BY id
        """,
        (session_id,)
    )

    history = cursor.fetchall()

    connection.close()

    return history


# --------------------------------
# Clear Current Session
# --------------------------------

def clear_history(session_id):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM conversations
        WHERE session_id = ?
        """,
        (session_id,)
    )

    connection.commit()

    connection.close()