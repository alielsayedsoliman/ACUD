from Configuration.config import Config

class RecruiterModel:
    @staticmethod
    def get_all_recruiters(page=1, items_per_page=10):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            # Get total count
            count_query = """
                SELECT COUNT(*) as total
                FROM recruiter
            """
            cursor.execute(count_query)
            total_items = cursor.fetchone().total

            # Calculate pagination values
            offset = (page - 1) * items_per_page

            query = """
                SELECT r.*, u.*
                FROM recruiter AS r
                INNER JOIN users AS u ON r.userID = u.userID
                ORDER BY r.userID
                OFFSET ? ROWS
                FETCH NEXT ? ROWS ONLY
            """
            cursor.execute(query, (offset, items_per_page))
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            recruiters = [dict(zip(columns, row)) for row in rows]

            cursor.close()
            conn.close()

            total_pages = (total_items + items_per_page - 1) // items_per_page
            
            return {
                "recruiters": recruiters,
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
    def insert_user_and_recruiter(data):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            insert_user_query = """
                INSERT INTO [users] 
                    (userID, first_name, middle_name, last_name, location, profile_pic, personal_summary, password, email)
                OUTPUT INSERTED.userID
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
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

            insert_recruiter_query = "INSERT INTO recruiter (userID) VALUES (?)"
            cursor.execute(insert_recruiter_query, (user_id,))

            conn.commit()
            cursor.close()
            conn.close()

            return {"message": "Recruiter registered successfully", "userID": user_id}

        except Exception as e:
            return {"error": str(e)}
