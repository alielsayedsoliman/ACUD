from Configuration.config import Config

class MentorModel:
    @staticmethod
    def get_all_mentors(page=1, items_per_page=10):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            # Get total count
            count_query = """
                SELECT COUNT(*) as total
                FROM mentor
            """
            cursor.execute(count_query)
            total_items = cursor.fetchone().total

            # Calculate pagination values
            offset = (page - 1) * items_per_page

            query = """
                SELECT m.*, u.*
                FROM mentor AS m
                INNER JOIN users AS u ON m.userID = u.userID
                ORDER BY m.userID
                OFFSET ? ROWS
                FETCH NEXT ? ROWS ONLY
            """
            cursor.execute(query, (offset, items_per_page))
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            mentors = [dict(zip(columns, row)) for row in rows]

            cursor.close()
            conn.close()

            total_pages = (total_items + items_per_page - 1) // items_per_page
            
            return {
                "mentors": mentors,
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
    def insert_user_and_mentor(data):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            insert_user_query = """
                INSERT INTO [users] 
                    (userID, first_name, middle_name, last_name, location, profile_pic, personal_summary, password, email)
                OUTPUT INSERTED.userID
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            # NOTE: password then email (order must match column list)
            cursor.execute(insert_user_query, (
                data["userID"],
                data["first_name"],
                data["middle_name"],
                data["last_name"],
                data["location"],
                data.get("profile_pic", None),
                data.get("personal_summary", None),
                data["password"],
                data["email"]
            ))

            user_id = cursor.fetchone()[0]

            insert_mentor_query = """
                INSERT INTO mentor (userID, professional_background, expertise) VALUES (?, ?, ?)
            """
            cursor.execute(insert_mentor_query, (
                user_id,
                data.get("professional_background", None),
                data.get("expertise", None)
            ))

            conn.commit()
            cursor.close()
            conn.close()

            return {"message": "Mentor registered successfully", "userID": user_id}

        except Exception as e:
            return {"error": str(e)}
