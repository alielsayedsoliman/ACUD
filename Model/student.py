from Configuration.config import Config


class StudentModel:
    @staticmethod
    def get_all_students():
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            query = """
                SELECT s.*, u.*
                FROM student AS s
                INNER JOIN users AS u ON s.userID = u.userID
            """
            cursor.execute(query)

            columns = [column[0] for column in cursor.description]  # get column names
            rows = cursor.fetchall()

            students = [dict(zip(columns, row)) for row in rows]

            cursor.close()
            conn.close()
            return students

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def insert_user_and_student(data):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            # Insert into Users table (with password)
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
                data.get("profile_pic", None),        # nullable
                data.get("personal_summary", None),   # nullable
                data["email"],
                data["password"]                     
            ))

            # Get the new UserID
            user_id = cursor.fetchone()[0]

            # Insert into Student_ table
            insert_student_query = "INSERT INTO student (userID) VALUES (?)"
            cursor.execute(insert_student_query, (user_id,))

            conn.commit()
            cursor.close()
            conn.close()

            return {"message": "Student registered successfully", "userID": user_id}

        except Exception as e:
            return {"error": str(e)}
