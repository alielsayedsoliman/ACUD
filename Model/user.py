# Model/user.py
from Configuration.config import Config

class UserModel:
    @staticmethod
    def get_all_users(page=1, items_per_page=10):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            # Get total count
            count_query = """
                SELECT COUNT(*) as total
                FROM users
            """
            cursor.execute(count_query)
            total_items = cursor.fetchone().total

            # Calculate pagination values
            offset = (page - 1) * items_per_page

            query = """
                SELECT u.*, 
                    CASE 
                        WHEN s.userID IS NOT NULL THEN 'student'
                        WHEN m.userID IS NOT NULL THEN 'mentor'
                        WHEN r.userID IS NOT NULL THEN 'recruiter'
                        ELSE 'user'
                    END as role
                FROM users u
                LEFT JOIN student s ON u.userID = s.userID
                LEFT JOIN mentor m ON u.userID = m.userID
                LEFT JOIN recruiter r ON u.userID = r.userID
                ORDER BY u.userID
                OFFSET ? ROWS
                FETCH NEXT ? ROWS ONLY
            """
            cursor.execute(query, (offset, items_per_page))
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            users = [dict(zip(columns, row)) for row in rows]

            cursor.close()
            conn.close()

            total_pages = (total_items + items_per_page - 1) // items_per_page
            
            return {
                "users": users,
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
    def login(email, password):
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            # 1. تحقق من وجود المستخدم
            query = """
                SELECT userID, password 
                FROM users 
                WHERE email = ?
            """
            cursor.execute(query, (email,))
            row = cursor.fetchone()

            if not row:
                return {"error": "Invalid email or password"}

            user_id, stored_password = row

            # (لو عايز تشفر الباسورد استبدل المقارنة دي بالـ hashing check)
            if stored_password != password:
                return {"error": "Invalid email or password"}

            # 2. تحديد الـ role
            role = "user"  # default

            cursor.execute("SELECT userID FROM student WHERE userID = ?", (user_id,))
            if cursor.fetchone():
                role = "student"
            else:
                cursor.execute("SELECT userID FROM mentor WHERE userID = ?", (user_id,))
                if cursor.fetchone():
                    role = "mentor"
                else:
                    cursor.execute("SELECT userID FROM recruiter WHERE userID = ?", (user_id,))
                    if cursor.fetchone():
                        role = "recruiter"

            cursor.close()
            conn.close()

            return {"message": "Login successful", "userID": user_id, "role": role}

        except Exception as e:
            return {"error": str(e)}
