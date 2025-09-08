from Configuration.config import Config

class MentorshipModel:
    @staticmethod
    def get_student(studentID):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            # Debug print
            print(f"Looking for student with ID: {studentID}")

            query = """
                SELECT u.userID, u.first_name, u.middle_name, u.last_name
                FROM users u
                JOIN student s ON u.userID = s.userID
                WHERE u.userID = ?
            """
            cursor.execute(query, (studentID,))
            student = cursor.fetchone()

            cursor.close()
            conn.close()
            
            if student:
                # Debug print to see the structure
                print(f"Student data: {student}")
                # Combine first, middle, and last name
                full_name = f"{student.first_name} {student.middle_name} {student.last_name}".strip()
                return {"userID": student.userID, "name": full_name}
            print(f"No student found with ID: {studentID}")
            return None
        except Exception as e:
            print(f"Error getting student: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    def get_mentor(mentorID):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            # Debug print
            print(f"Looking for mentor with ID: {mentorID}")

            query = """
                SELECT u.userID, u.first_name, u.middle_name, u.last_name
                FROM users u
                JOIN mentor m ON u.userID = m.userID
                WHERE u.userID = ?
            """
            cursor.execute(query, (mentorID,))
            mentor = cursor.fetchone()

            cursor.close()
            conn.close()
            
            if mentor:
                # Debug print to see the structure
                print(f"Mentor data: {mentor}")
                # Combine first, middle, and last name
                full_name = f"{mentor.first_name} {mentor.middle_name} {mentor.last_name}".strip()
                return {"userID": mentor.userID, "name": full_name}
            print(f"No mentor found with ID: {mentorID}")
            return None
        except Exception as e:
            print(f"Error getting mentor: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    def create_mentorship(studentID, mentorID):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            # First check if mentorship already exists
            check_query = """
                SELECT COUNT(*) 
                FROM MentorshipRequests 
                WHERE studentID = ? AND mentorID = ?
            """
            cursor.execute(check_query, (studentID, mentorID))
            count = cursor.fetchone()[0]

            if count > 0:
                cursor.close()
                conn.close()
                return {"status": "exists", "message": "Mentorship already exists"}

            # If not exists, create new mentorship
            query = """
                INSERT INTO MentorshipRequests (studentID, mentorID)
                VALUES (?, ?)
            """
            cursor.execute(query, (studentID, mentorID))
            conn.commit()

            cursor.close()
            conn.close()
            return {"status": "created", "message": "Mentorship created successfully"}
        except Exception as e:
            print(f"Error creating mentorship: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    def get_mentor_requests(mentorID, page=1, items_per_page=10):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            # First get total count
            count_query = """
                SELECT COUNT(*) as total
                FROM MentorshipRequests mr
                WHERE mr.mentorID = ?
            """
            cursor.execute(count_query, (mentorID,))
            total_items = cursor.fetchone().total

            # Calculate pagination values
            offset = (page - 1) * items_per_page

            # Get paginated data
            query = """
                SELECT mr.requestID, mr.studentID, mr.mentorID, 
                       u.first_name, u.middle_name, u.last_name,
                       u.email, u.personal_summary
                FROM MentorshipRequests mr
                JOIN users u ON mr.studentID = u.userID
                WHERE mr.mentorID = ?
                ORDER BY mr.requestID
                OFFSET ? ROWS
                FETCH NEXT ? ROWS ONLY
            """
            cursor.execute(query, (mentorID, offset, items_per_page))
            
            requests = []
            for row in cursor.fetchall():
                full_name = f"{row.first_name} {row.middle_name} {row.last_name}".strip()
                requests.append({
                    "requestID": row.requestID,
                    "studentID": row.studentID,
                    "studentName": full_name,
                    "studentEmail": row.email,
                    "studentSummary": row.personal_summary
                })

            cursor.close()
            conn.close()

            total_pages = (total_items + items_per_page - 1) // items_per_page
            
            return {
                "requests": requests,
                "pagination": {
                    "total_items": total_items,
                    "total_pages": total_pages,
                    "current_page": page,
                    "items_per_page": items_per_page
                }
            }
        except Exception as e:
            print(f"Error getting mentor requests: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    def get_mentor_students(mentorID, page=1, items_per_page=10):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            # First get total count
            count_query = """
                SELECT COUNT(*) as total
                FROM users u
                JOIN student s ON u.userID = s.userID
                JOIN MentorshipRequests mr ON s.userID = mr.studentID
                WHERE mr.mentorID = ?
            """
            cursor.execute(count_query, (mentorID,))
            total_items = cursor.fetchone().total

            # Calculate pagination values
            offset = (page - 1) * items_per_page

            # Get paginated data
            query = """
                SELECT u.userID, u.first_name, u.middle_name, u.last_name,
                       u.email, u.personal_summary
                FROM users u
                JOIN student s ON u.userID = s.userID
                JOIN MentorshipRequests mr ON s.userID = mr.studentID
                WHERE mr.mentorID = ?
                ORDER BY u.userID
                OFFSET ? ROWS
                FETCH NEXT ? ROWS ONLY
            """
            cursor.execute(query, (mentorID, offset, items_per_page))
            
            students = []
            for row in cursor.fetchall():
                full_name = f"{row.first_name} {row.middle_name} {row.last_name}".strip()
                students.append({
                    "userID": row.userID,
                    "name": full_name,
                    "email": row.email,
                    "summary": row.personal_summary
                })

            cursor.close()
            conn.close()

            total_pages = (total_items + items_per_page - 1) // items_per_page
            
            return {
                "students": students,
                "pagination": {
                    "total_items": total_items,
                    "total_pages": total_pages,
                    "current_page": page,
                    "items_per_page": items_per_page
                }
            }
        except Exception as e:
            print(f"Error getting mentor students: {str(e)}")
            return {"error": str(e)}
