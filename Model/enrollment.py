# Model/enrollment.py (نكمل عليه اللي موجود)
from Configuration.config import Config

class EnrollmentModel:
    @staticmethod
    def enroll_course(student_id, course_id):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO course_enrollment 
                    (coursesID, userID, current_status, enrollment_date) 
                VALUES 
                    (?, ?, 'enrolled', GETDATE())
            """
            cursor.execute(query, (course_id, student_id))

            conn.commit()
            cursor.close()
            conn.close()

            return {"message": "Student enrolled in course successfully"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def enroll_internship(student_id, internship_id):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO internship_enrollment 
                    (internshipID, studentID, current_status, enrollment_date) 
                VALUES 
                    (?, ?, 'enrolled', GETDATE())
            """
            cursor.execute(query, (internship_id, student_id))

            conn.commit()
            cursor.close()
            conn.close()

            return {"message": "Student enrolled in internship successfully"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_student_courses(student_id, page=1, items_per_page=10):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            # Get total count
            count_query = """
                SELECT COUNT(*) as total
                FROM course_enrollment
                WHERE userID = ?
            """
            cursor.execute(count_query, (student_id,))
            total_items = cursor.fetchone().total

            # Calculate pagination values
            offset = (page - 1) * items_per_page

            query = """
                SELECT c.*, ce.enrollment_date
                FROM course_enrollment AS ce
                INNER JOIN courses AS c ON ce.coursesID = c.coursesID
                WHERE ce.userID = ?
                ORDER BY ce.enrollment_date DESC
                OFFSET ? ROWS
                FETCH NEXT ? ROWS ONLY
            """
            cursor.execute(query, (student_id, offset, items_per_page))
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            courses = [dict(zip(columns, row)) for row in rows]

            cursor.close()
            conn.close()

            total_pages = (total_items + items_per_page - 1) // items_per_page
            
            return {
                "courses": courses,
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
    def get_student_internships(student_id, page=1, items_per_page=10):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            # Get total count
            count_query = """
                SELECT COUNT(*) as total
                FROM internship_enrollment
                WHERE studentID = ?
            """
            cursor.execute(count_query, (student_id,))
            total_items = cursor.fetchone().total

            # Calculate pagination values
            offset = (page - 1) * items_per_page

            query = """
                SELECT i.*, ie.enrollment_date
                FROM internship_enrollment AS ie
                INNER JOIN internship AS i ON ie.internshipID = i.internshipID
                WHERE ie.studentID = ?
                ORDER BY ie.enrollment_date DESC
                OFFSET ? ROWS
                FETCH NEXT ? ROWS ONLY
            """
            cursor.execute(query, (student_id, offset, items_per_page))
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
