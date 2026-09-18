from app.database.database import get_connection


def show_opportunities():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            company,
            role,
            source,
            stage,
            status,
            priority,
            next_action
        FROM opportunities
        ORDER BY id DESC
    """)

    opportunities = cursor.fetchall()

    connection.close()

    if not opportunities:
        print("No opportunities found.")
        return

    print("\n========== JOBHUNT AI OPPORTUNITIES ==========\n")

    for opportunity in opportunities:
        print(f"ID: {opportunity['id']}")
        print(f"Company: {opportunity['company']}")
        print(f"Role: {opportunity['role']}")
        print(f"Source: {opportunity['source']}")
        print(f"Stage: {opportunity['stage']}")
        print(f"Status: {opportunity['status']}")
        print(f"Priority: {opportunity['priority'] or 'Not set'}")
        print(f"Next Action: {opportunity['next_action'] or 'Not set'}")
        print("----------------------------------------------")


if __name__ == "__main__":
    show_opportunities()