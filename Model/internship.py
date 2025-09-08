# Model/internship.py
from Configuration.config import Config

class InternshipModel:
    @staticmethod
    def get_all_internships(page=1, items_per_page=10):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            # Get total count
            count_query = """
                SELECT COUNT(*) as total
                FROM internship
            """
            cursor.execute(count_query)
            total_items = cursor.fetchone().total

            # Calculate pagination values
            offset = (page - 1) * items_per_page

            query = """
                SELECT i.*, u.first_name, u.last_name, u.email
                FROM internship AS i
                INNER JOIN recruiter AS r ON i.recruiterID = r.userID
                INNER JOIN users AS u ON r.userID = u.userID
                ORDER BY i.internshipID
                OFFSET ? ROWS
                FETCH NEXT ? ROWS ONLY
            """
            cursor.execute(query, (offset, items_per_page))
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            internships = [dict(zip(columns, row)) for row in rows]

            cursor.close()
            conn.close()

            total_pages = (total_items + items_per_page - 1) // items_per_page
            
            return {
                "internships": internships,
                "pagination": {
                    "total_items": total_items,
                    "total_pages": total_pages,
                    "current_page": page,
                    "items_per_page": items_per_page
                }
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def create_internship(data):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO internship (recruiterID, title, description, location, start_date, end_date)
                OUTPUT INSERTED.internshipID
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                data["recruiterID"],
                data["title"],
                data.get("description", None),
                data.get("location", None),
                data.get("start_date", None),
                data.get("end_date", None)
            ))

            internship_id = cursor.fetchone()[0]

            conn.commit()
            cursor.close()
            conn.close()
            return {"internshipID": internship_id, "message": "Internship created successfully"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_internship(internshipID, data):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            # First check if internship exists and get current values
            check_query = """
                SELECT * FROM internship WHERE internshipID = ?
            """
            cursor.execute(check_query, (internshipID,))
            existing = cursor.fetchone()

            if not existing:
                cursor.close()
                conn.close()
                return {"error": "Internship not found"}

            # Build update query based on provided fields
            update_fields = []
            params = []
            if "title" in data:
                update_fields.append("title = ?")
                params.append(data["title"])
            if "description" in data:
                update_fields.append("description = ?")
                params.append(data["description"])
            if "location" in data:
                update_fields.append("location = ?")
                params.append(data["location"])
            if "start_date" in data:
                update_fields.append("start_date = ?")
                params.append(data["start_date"])
            if "end_date" in data:
                update_fields.append("end_date = ?")
                params.append(data["end_date"])

            if not update_fields:
                return {"error": "No fields to update"}

            # Add internshipID to params
            params.append(internshipID)

            # Execute update query
            update_query = f"""
                UPDATE internship 
                SET {', '.join(update_fields)}
                WHERE internshipID = ?
            """
            cursor.execute(update_query, params)
            conn.commit()

            cursor.close()
            conn.close()
            return {"message": "Internship updated successfully"}
        except Exception as e:
            print(f"Error updating internship: {str(e)}")
            return {"error": str(e)}
