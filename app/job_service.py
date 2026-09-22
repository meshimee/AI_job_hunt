from datetime import datetime
from typing import Optional

from app.database.database import get_connection


def add_job(
    company: str,
    role: str = "",
    contact_name: str = "",
    contact_role: str = "",
    source: str = "",
    stage: str = "Saved",
    status: str = "Active",
    priority: str = "Medium",
    deadline: str = "",
    next_action: str = "",
    notes: str = "",
):
    """
    Add a new job opportunity.

    Returns:
        int: ID of the newly created opportunity.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO opportunities (
            company,
            role,
            contact_name,
            contact_role,
            source,
            stage,
            status,
            priority,
            deadline,
            next_action,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            company,
            role,
            contact_name,
            contact_role,
            source,
            stage,
            status,
            priority,
            deadline,
            next_action,
            notes,
        ),
    )

    opportunity_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return opportunity_id


def get_all_jobs():
    """
    Retrieve all job opportunities.

    Returns:
        list: List of opportunity dictionaries.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM opportunities
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()

    jobs = [dict(row) for row in rows]

    connection.close()

    return jobs


def get_job_by_id(job_id: int):
    """
    Retrieve a single job opportunity by ID.

    Args:
        job_id: Opportunity ID.

    Returns:
        dict | None
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM opportunities
        WHERE id = ?
        """,
        (job_id,),
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)


def update_job(
    job_id: int,
    company: Optional[str] = None,
    role: Optional[str] = None,
    contact_name: Optional[str] = None,
    contact_role: Optional[str] = None,
    source: Optional[str] = None,
    stage: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    deadline: Optional[str] = None,
    next_action: Optional[str] = None,
    notes: Optional[str] = None,
):
    """
    Update an existing job opportunity.

    Only fields passed to the function will be updated.

    Returns:
        bool: True if updated successfully.
    """

    fields = []
    values = []

    if company is not None:
        fields.append("company = ?")
        values.append(company)

    if role is not None:
        fields.append("role = ?")
        values.append(role)

    if contact_name is not None:
        fields.append("contact_name = ?")
        values.append(contact_name)

    if contact_role is not None:
        fields.append("contact_role = ?")
        values.append(contact_role)

    if source is not None:
        fields.append("source = ?")
        values.append(source)

    if stage is not None:
        fields.append("stage = ?")
        values.append(stage)

    if status is not None:
        fields.append("status = ?")
        values.append(status)

    if priority is not None:
        fields.append("priority = ?")
        values.append(priority)

    if deadline is not None:
        fields.append("deadline = ?")
        values.append(deadline)

    if next_action is not None:
        fields.append("next_action = ?")
        values.append(next_action)

    if notes is not None:
        fields.append("notes = ?")
        values.append(notes)

    if not fields:
        return False

    fields.append("updated_at = CURRENT_TIMESTAMP")

    values.append(job_id)

    connection = get_connection()
    cursor = connection.cursor()

    query = f"""
        UPDATE opportunities
        SET {", ".join(fields)}
        WHERE id = ?
    """

    cursor.execute(query, values)

    updated = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return updated


def delete_job(job_id: int):
    """
    Delete a job opportunity.

    Returns:
        bool: True if deleted successfully.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM opportunities
        WHERE id = ?
        """,
        (job_id,),
    )

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted


def search_jobs(keyword: str):
    """
    Search opportunities by company, role, source,
    status, priority or notes.

    Returns:
        list: Matching opportunities.
    """

    connection = get_connection()
    cursor = connection.cursor()

    search_pattern = f"%{keyword}%"

    cursor.execute(
        """
        SELECT *
        FROM opportunities
        WHERE
            company LIKE ?
            OR role LIKE ?
            OR source LIKE ?
            OR status LIKE ?
            OR priority LIKE ?
            OR notes LIKE ?
        ORDER BY created_at DESC
        """,
        (
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern,
        ),
    )

    rows = cursor.fetchall()

    jobs = [dict(row) for row in rows]

    connection.close()

    return jobs


def update_job_status(job_id: int, status: str):
    """
    Update the status of a job opportunity.

    Example:
        Active
        On Hold
        Closed
        Rejected
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE opportunities
        SET
            status = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (status, job_id),
    )

    updated = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return updated


def update_job_stage(job_id: int, stage: str):
    """
    Update the application stage.

    Example:
        Saved
        Shortlisted
        Applied
        HR Screen
        Technical Interview
        Final Interview
        Offer
        Rejected
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE opportunities
        SET
            stage = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (stage, job_id),
    )

    updated = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return updated