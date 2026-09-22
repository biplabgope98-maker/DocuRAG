import sqlite3
import os

from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DATABASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(DATABASE_DIR, "docurag.db")


def get_db_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def create_default_admin(connection):
    """
    Create the default admin account if no admin account exists.

    Admin credentials are read from environment variables:
        ADMIN_USERNAME
        ADMIN_EMAIL
        ADMIN_PASSWORD

    This function is safe to run every time the application starts.
    It will not create duplicate admin accounts.
    """

    admin_exists = connection.execute(
        """
        SELECT id
        FROM users
        WHERE role = 'admin'
        LIMIT 1
        """
    ).fetchone()

    # Admin already exists
    if admin_exists:
        return

    admin_username = os.getenv("ADMIN_USERNAME")
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_username or not admin_email or not admin_password:
        raise RuntimeError(
            "Default admin cannot be created. "
            "Please configure ADMIN_USERNAME, ADMIN_EMAIL, "
            "and ADMIN_PASSWORD in the .env file."
        )

    admin_username = admin_username.strip()
    admin_email = admin_email.strip().lower()

    if not admin_username or not admin_email:
        raise RuntimeError(
            "ADMIN_USERNAME and ADMIN_EMAIL cannot be empty."
        )

    # Same password policy used by the previous manual admin creation
    if len(admin_password) < 8:
        raise RuntimeError(
            "ADMIN_PASSWORD must contain at least 8 characters."
        )

    if not any(c.isupper() for c in admin_password):
        raise RuntimeError(
            "ADMIN_PASSWORD must contain an uppercase letter."
        )

    if not any(c.islower() for c in admin_password):
        raise RuntimeError(
            "ADMIN_PASSWORD must contain a lowercase letter."
        )

    if not any(c.isdigit() for c in admin_password):
        raise RuntimeError(
            "ADMIN_PASSWORD must contain a number."
        )

    if not any(not c.isalnum() for c in admin_password):
        raise RuntimeError(
            "ADMIN_PASSWORD must contain a special character."
        )

    # Prevent collision with an existing normal user
    existing_user = connection.execute(
        """
        SELECT id, username, email
        FROM users
        WHERE username = ? OR email = ?
        LIMIT 1
        """,
        (admin_username, admin_email)
    ).fetchone()

    if existing_user:
        raise RuntimeError(
            "Cannot create default admin because the configured "
            "ADMIN_USERNAME or ADMIN_EMAIL is already used by another account."
        )

    password_hash = generate_password_hash(admin_password)

    connection.execute(
        """
        INSERT INTO users (
            username,
            email,
            password_hash,
            role,
            is_active
        )
        VALUES (?, ?, ?, 'admin', 1)
        """,
        (
            admin_username,
            admin_email,
            password_hash
        )
    )

    print("========================================")
    print("Default admin account created successfully")
    print(f"Admin username: {admin_username}")
    print(f"Admin email   : {admin_email}")
    print("Admin role    : admin")
    print("========================================")

def init_db():

    os.makedirs(DATABASE_DIR, exist_ok=True)

    connection = get_db_connection()
    cursor = connection.cursor()

    # Users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(120) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL DEFAULT 'user',
            is_active BOOLEAN NOT NULL DEFAULT 1,
            last_login DATETIME,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Documents
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename VARCHAR(255) NOT NULL,
            original_filename VARCHAR(255) NOT NULL,
            file_type VARCHAR(50) NOT NULL,
            file_size INTEGER NOT NULL,
            file_path VARCHAR(500) NOT NULL,
            upload_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            uploader_id INTEGER NOT NULL,
            processing_status VARCHAR(30) NOT NULL DEFAULT 'uploaded',
            page_count INTEGER,
            error_message VARCHAR(1000),
            content_hash VARCHAR(64) NOT NULL,
            processed_at DATETIME,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (uploader_id)
                REFERENCES users(id)
        )
    """)

    # Document Chunks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            page_number INTEGER NOT NULL,
            position INTEGER NOT NULL,
            embedding BLOB,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (document_id)
                REFERENCES documents(id)
                ON DELETE CASCADE
        )
    """)

    # Image Analysis
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS image_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER NOT NULL,
            page_number INTEGER NOT NULL,
            image_index INTEGER NOT NULL,
            image_path VARCHAR(500),
            image_type VARCHAR(100),
            objects TEXT,
            extracted_text TEXT,
            orientation VARCHAR(100),
            colors TEXT,
            anomalies TEXT,
            description TEXT,
            raw_analysis TEXT,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (document_id)
                REFERENCES documents(id)
                ON DELETE CASCADE
        )
    """)

    # Queries
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            conversation_id VARCHAR(100) NOT NULL,
            question TEXT NOT NULL,
            answer TEXT,
            confidence FLOAT,
            response_time FLOAT,
            cache_hit BOOLEAN NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)

    # Query Sources
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS query_sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_id INTEGER NOT NULL,
            document_id INTEGER NOT NULL,
            chunk_id INTEGER,
            similarity FLOAT,
            source_page INTEGER,
            retrieved_text TEXT,
            image_context TEXT,
            rank INTEGER,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (query_id)
                REFERENCES queries(id)
                ON DELETE CASCADE,

            FOREIGN KEY (document_id)
                REFERENCES documents(id)
                ON DELETE CASCADE,

            FOREIGN KEY (chunk_id)
                REFERENCES document_chunks(id)
                ON DELETE SET NULL
        )
    """)

    # Indexes
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_documents_uploader
        ON documents(uploader_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_documents_status
        ON documents(processing_status)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_chunks_document
        ON document_chunks(document_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_chunks_page
        ON document_chunks(page_number)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_images_document
        ON image_analysis(document_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_queries_user
        ON queries(user_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_queries_conversation
        ON queries(conversation_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sources_query
        ON query_sources(query_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sources_document
        ON query_sources(document_id)
    """)

    # Create the default admin account if one does not exist
    create_default_admin(connection)

    connection.commit()
    connection.close()

    print("Database initialized successfully.")
    print(f"Database location: {DATABASE_PATH}")

if __name__ == "__main__":
    init_db()
