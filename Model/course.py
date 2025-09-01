from Configuration.config import Config


class CourseModel:
    @staticmethod
    def get_all_courses():
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            query = """
                SELECT coursesID, title, brief_description, difficulty_level
                FROM courses
            """
            cursor.execute(query)

            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()

            courses = [dict(zip(columns, row)) for row in rows]

            cursor.close()
            conn.close()
            return courses

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_course_by_id(course_id):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            query = """
                SELECT coursesID, title, brief_description, difficulty_level
                FROM courses
                WHERE coursesID = ?
            """
            cursor.execute(query, (course_id,))

            row = cursor.fetchone()
            if row:
                columns = [column[0] for column in cursor.description]
                course = dict(zip(columns, row))
            else:
                course = None

            cursor.close()
            conn.close()
            return course

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def create_course(data):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            insert_query = """
                INSERT INTO courses (coursesID, title, brief_description, difficulty_level)
                OUTPUT INSERTED.coursesID
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(insert_query, (
                data["coursesID"],
                data["title"],
                data["brief_description"],
                data["difficulty_level"]
            ))

            course_id = cursor.fetchone()[0]

            conn.commit()
            cursor.close()
            conn.close()

            return {"message": "Course created successfully", "coursesID": course_id}

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_course(course_id, data):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            update_query = """
                UPDATE courses
                SET title = ?,
                    brief_description = ?,
                    difficulty_level = ?
                WHERE coursesID = ?
            """
            cursor.execute(update_query, (
                data["title"],
                data["brief_description"],
                data["difficulty_level"],
                course_id
            ))

            if cursor.rowcount == 0:
                return {"error": "Course not found"}

            conn.commit()
            cursor.close()
            conn.close()

            return {"message": "Course updated successfully"}

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_course(course_id):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            delete_query = "DELETE FROM courses WHERE coursesID = ?"
            cursor.execute(delete_query, (course_id,))

            if cursor.rowcount == 0:
                return {"error": "Course not found"}

            conn.commit()
            cursor.close()
            conn.close()

            return {"message": "Course deleted successfully"}

        except Exception as e:
            return {"error": str(e)}
