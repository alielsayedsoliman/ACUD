from Configuration.config import Config


class StudentModel:
    @staticmethod
    def get_all_students():
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            query = """
                SELECT s.*, u.*
                FROM Student_ AS s
                INNER JOIN Users AS u ON s.User_ID = u.User_ID
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

            # Insert into User table
            insert_user_query = """
                INSERT INTO [Users] (User_ID, name, phone_number, email, location, password)
                OUTPUT INSERTED.User_ID
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_user_query, (
                data["User_ID"],
                data["name"],
                data["phone_number"],
                data["email"],
                data["location"],
                data["password"]
            ))

            # Get the new User_ID
            user_id = cursor.fetchone()[0]

            # Insert into Student_ table
            insert_student_query = "INSERT INTO Student_ (User_ID) VALUES (?)"
            cursor.execute(insert_student_query, (user_id,))

            conn.commit()
            cursor.close()
            conn.close()

            return {"message": "Student registered successfully", "User_ID": user_id}

        except Exception as e:
            return {"error": str(e)}
