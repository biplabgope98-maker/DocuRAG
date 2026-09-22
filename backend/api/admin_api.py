import os
import sys
import shutil

from fastapi import APIRouter, HTTPException, Header

# ============================================================
# PATH SETUP
# ============================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

BACKEND_ROOT = os.path.dirname(
    CURRENT_DIR
)

PROJECT_ROOT = os.path.dirname(
    BACKEND_ROOT
)

sys.path.insert(0, BACKEND_ROOT)
sys.path.insert(0, PROJECT_ROOT)


from database.database import get_db_connection
from backend.services.vector_store import rebuild_index

# Reuse existing JWT authentication
from backend.api.auth_api import get_user_from_token


# ============================================================
# ROUTER
# ============================================================

admin_router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"]
)


# ============================================================
# ADMIN AUTHENTICATION
# ============================================================

def require_admin(
    authorization: str = Header(default=None)
):
    """
    Verify JWT token and make sure the logged-in
    user is an administrator.
    """

    payload = get_user_from_token(
        authorization
    )

    user_id = int(
        payload["sub"]
    )

    connection = get_db_connection()

    try:

        user = connection.execute(
            """
            SELECT
                id,
                username,
                email,
                role,
                is_active
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        ).fetchone()

        if not user:

            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        if not user["is_active"]:

            raise HTTPException(
                status_code=403,
                detail="Account is inactive"
            )

        if user["role"] != "admin":

            raise HTTPException(
                status_code=403,
                detail="Admin access required"
            )

        return user

    finally:

        connection.close()


# ============================================================
# ADMIN HEALTH
# ============================================================

@admin_router.get("/health")
def admin_health(
    authorization: str = Header(default=None)
):

    require_admin(
        authorization
    )

    return {
        "status": "success",
        "message": "Admin API is working"
    }


# ============================================================
# ADMIN STATISTICS
# ============================================================

@admin_router.get("/statistics")
def get_statistics(
    authorization: str = Header(default=None)
):

    require_admin(
        authorization
    )

    connection = get_db_connection()

    try:

        total_users = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM users
            """
        ).fetchone()["count"]

        active_users = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM users
            WHERE is_active = 1
            """
        ).fetchone()["count"]

        inactive_users = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM users
            WHERE is_active = 0
            """
        ).fetchone()["count"]

        admin_users = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM users
            WHERE role = 'admin'
            """
        ).fetchone()["count"]

        total_documents = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM documents
            """
        ).fetchone()["count"]

        processed_documents = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM documents
            WHERE processing_status = 'processed'
            """
        ).fetchone()["count"]

        failed_documents = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM documents
            WHERE processing_status = 'failed'
            """
        ).fetchone()["count"]

        processing_documents = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM documents
            WHERE processing_status IN (
                'uploaded',
                'processing'
            )
            """
        ).fetchone()["count"]

        total_queries = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM queries
            """
        ).fetchone()["count"]

        cached_queries = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM queries
            WHERE cache_hit = 1
            """
        ).fetchone()["count"]

        return {
            "status": "success",
            "statistics": {
                "users": {
                    "total": total_users,
                    "active": active_users,
                    "inactive": inactive_users,
                    "admins": admin_users
                },
                "documents": {
                    "total": total_documents,
                    "processed": processed_documents,
                    "failed": failed_documents,
                    "processing": processing_documents
                },
                "queries": {
                    "total": total_queries,
                    "cache_hits": cached_queries
                }
            }
        }

    finally:

        connection.close()


# ============================================================
# GET USERS
# ============================================================

@admin_router.get("/users")
def get_users(
    authorization: str = Header(default=None)
):

    require_admin(
        authorization
    )

    connection = get_db_connection()

    try:

        users = connection.execute(
            """
            SELECT
                id,
                username,
                email,
                role,
                is_active,
                last_login,
                created_at,
                updated_at
            FROM users
            ORDER BY created_at DESC
            """
        ).fetchall()

        return {
            "status": "success",
            "count": len(users),
            "users": [
                dict(user)
                for user in users
            ]
        }

    finally:

        connection.close()


# ============================================================
# ACTIVATE USER
# ============================================================

@admin_router.put("/users/{user_id}/activate")
def activate_user(
    user_id: int,
    authorization: str = Header(default=None)
):

    current_admin = require_admin(
        authorization
    )

    connection = get_db_connection()

    try:

        user = connection.execute(
            """
            SELECT id, username, is_active
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        ).fetchone()

        if not user:

            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        connection.execute(
            """
            UPDATE users
            SET is_active = 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (user_id,)
        )

        connection.commit()

        return {
            "status": "success",
            "message": "User activated successfully",
            "user_id": user_id
        }

    finally:

        connection.close()


# ============================================================
# DEACTIVATE USER
# ============================================================

@admin_router.put("/users/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    authorization: str = Header(default=None)
):

    current_admin = require_admin(
        authorization
    )

    connection = get_db_connection()

    try:

        user = connection.execute(
            """
            SELECT id, username, role, is_active
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        ).fetchone()

        if not user:

            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        # Prevent admin from disabling himself
        if user_id == current_admin["id"]:

            raise HTTPException(
                status_code=400,
                detail="You cannot deactivate your own admin account"
            )

        connection.execute(
            """
            UPDATE users
            SET is_active = 0,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (user_id,)
        )

        connection.commit()

        return {
            "status": "success",
            "message": "User deactivated successfully",
            "user_id": user_id
        }

    finally:

        connection.close()


# ============================================================
# DELETE USER
# ============================================================

@admin_router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    authorization: str = Header(default=None)
):

    current_admin = require_admin(
        authorization
    )

    connection = get_db_connection()

    try:

        user = connection.execute(
            """
            SELECT
                id,
                username,
                email,
                role
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        ).fetchone()

        if not user:

            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        # Prevent deleting own account
        if user_id == current_admin["id"]:

            raise HTTPException(
                status_code=400,
                detail="You cannot delete your own admin account"
            )

        connection.execute(
            """
            DELETE FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        connection.commit()

        return {
            "status": "success",
            "message": "User deleted successfully",
            "user_id": user_id
        }

    finally:

        connection.close()


# ============================================================
# GET ALL DOCUMENTS
# ============================================================

@admin_router.get("/documents")
def get_documents(
    authorization: str = Header(default=None)
):

    require_admin(
        authorization
    )

    connection = get_db_connection()

    try:

        documents = connection.execute(
            """
            SELECT
                d.id,
                d.filename,
                d.original_filename,
                d.file_type,
                d.file_size,
                d.upload_date,
                d.uploader_id,
                u.username AS uploader_username,
                u.email AS uploader_email,
                d.processing_status,
                d.page_count,
                d.error_message,
                d.content_hash,
                d.processed_at,
                d.created_at,
                d.updated_at
            FROM documents d
            LEFT JOIN users u
                ON d.uploader_id = u.id
            ORDER BY d.created_at DESC
            """
        ).fetchall()

        return {
            "status": "success",
            "count": len(documents),
            "documents": [
                dict(document)
                for document in documents
            ]
        }

    finally:

        connection.close()


# ============================================================
# DELETE DOCUMENT
# ============================================================

@admin_router.delete("/documents/{document_id}")
def delete_admin_document(
    document_id: int,
    authorization: str = Header(default=None)
):
    """Permanently delete a document as an administrator."""

    require_admin(authorization)

    connection = get_db_connection()
    file_path = None
    document_name = None

    try:
        document = connection.execute(
            """
            SELECT id, original_filename, file_path
            FROM documents
            WHERE id = ?
            """,
            (document_id,)
        ).fetchone()

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

        file_path = document["file_path"]
        document_name = document["original_filename"]

        connection.execute(
            "DELETE FROM query_sources WHERE document_id = ?",
            (document_id,)
        )
        connection.execute(
            "DELETE FROM image_analysis WHERE document_id = ?",
            (document_id,)
        )
        connection.execute(
            "DELETE FROM document_chunks WHERE document_id = ?",
            (document_id,)
        )
        connection.execute(
            "DELETE FROM documents WHERE id = ?",
            (document_id,)
        )

        connection.commit()

    except HTTPException:
        connection.rollback()
        raise

    except Exception as e:
        connection.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Could not delete document: {str(e)}"
        )

    finally:
        connection.close()

    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(
            f"Warning: Could not delete physical file for document {document_id}: {e}"
        )

    try:
        extracted_images_dir = os.path.join(
            PROJECT_ROOT,
            "uploads",
            f"extracted_images_{document_id}"
        )
        if os.path.exists(extracted_images_dir):
            shutil.rmtree(extracted_images_dir, ignore_errors=True)
    except Exception as e:
        print(
            f"Warning: Could not delete extracted images for document {document_id}: {e}"
        )

    try:
        rebuild_index()
    except Exception as e:
        print("Warning: Could not rebuild vector index:", e)

    return {
        "status": "success",
        "message": f'Document "{document_name}" deleted successfully.',
        "document_id": document_id
    }


# ============================================================
# PROCESSING FAILURES
# ============================================================

@admin_router.get("/processing-failures")
def get_processing_failures(
    authorization: str = Header(default=None)
):

    require_admin(
        authorization
    )

    connection = get_db_connection()

    try:

        failures = connection.execute(
            """
            SELECT
                d.id,
                d.original_filename,
                d.file_type,
                d.file_size,
                d.upload_date,
                d.uploader_id,
                u.username AS uploader_username,
                d.processing_status,
                d.error_message,
                d.page_count,
                d.updated_at
            FROM documents d
            LEFT JOIN users u
                ON d.uploader_id = u.id
            WHERE d.processing_status = 'failed'
            ORDER BY d.updated_at DESC
            """
        ).fetchall()

        return {
            "status": "success",
            "count": len(failures),
            "failures": [
                dict(failure)
                for failure in failures
            ]
        }

    finally:

        connection.close()


# ============================================================
# GET ALL QUERIES
# ============================================================

@admin_router.get("/queries")
def get_queries(
    authorization: str = Header(default=None)
):

    require_admin(
        authorization
    )

    connection = get_db_connection()

    try:

        queries = connection.execute(
            """
            SELECT
                q.id,
                q.user_id,
                u.username,
                u.email,
                q.conversation_id,
                q.question,
                q.answer,
                q.confidence,
                q.response_time,
                q.cache_hit,
                q.created_at
            FROM queries q
            LEFT JOIN users u
                ON q.user_id = u.id
            ORDER BY q.created_at DESC
            LIMIT 100
            """
        ).fetchall()

        return {
            "status": "success",
            "count": len(queries),
            "queries": [
                dict(query)
                for query in queries
            ]
        }

    finally:

        connection.close()


# ============================================================
# DELETE QUERY
# ============================================================

@admin_router.delete("/queries/{query_id}")
def delete_admin_query(
    query_id: int,
    authorization: str = Header(default=None)
):
    """Permanently delete a query and its source references as an administrator."""

    require_admin(authorization)

    connection = get_db_connection()

    try:
        query = connection.execute(
            """
            SELECT id, question
            FROM queries
            WHERE id = ?
            """,
            (query_id,)
        ).fetchone()

        if not query:
            raise HTTPException(
                status_code=404,
                detail="Query not found."
            )

        connection.execute(
            "DELETE FROM query_sources WHERE query_id = ?",
            (query_id,)
        )

        connection.execute(
            "DELETE FROM queries WHERE id = ?",
            (query_id,)
        )

        connection.commit()

        return {
            "status": "success",
            "message": "Query deleted successfully.",
            "query_id": query_id
        }

    except HTTPException:
        connection.rollback()
        raise

    except Exception as e:
        connection.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Could not delete query: {str(e)}"
        )

    finally:
        connection.close()


# ============================================================
# DOCUMENT DETAILS
# ============================================================

@admin_router.get("/documents/{document_id}")
def get_document_details(
    document_id: int,
    authorization: str = Header(default=None)
):

    require_admin(
        authorization
    )

    connection = get_db_connection()

    try:

        document = connection.execute(
            """
            SELECT
                d.*,
                u.username AS uploader_username,
                u.email AS uploader_email
            FROM documents d
            LEFT JOIN users u
                ON d.uploader_id = u.id
            WHERE d.id = ?
            """,
            (document_id,)
        ).fetchone()

        if not document:

            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        chunks_count = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM document_chunks
            WHERE document_id = ?
            """,
            (document_id,)
        ).fetchone()["count"]

        images_count = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM image_analysis
            WHERE document_id = ?
            """,
            (document_id,)
        ).fetchone()["count"]

        return {
            "status": "success",
            "document": dict(document),
            "statistics": {
                "chunks": chunks_count,
                "image_analysis": images_count
            }
        }

    finally:

        connection.close()