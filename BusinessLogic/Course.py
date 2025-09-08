from Model.course import CourseModel

class CourseService:
    @staticmethod
    def fetch_all_courses(page=1, items_per_page=10):
        result = CourseModel.get_all_courses(page, items_per_page)
        # Add any business logic here (filtering, sorting, etc.)
        return result

    @staticmethod
    def get_course(course_id):
        if not course_id:
            return {"error": "Course ID is required"}
        
        course = CourseModel.get_course_by_id(course_id)
        if not course:
            return {"error": "Course not found"}
        
        return course

    @staticmethod
    def create_course(data):
        # Validate required fields
        required_fields = ["coursesID", "title", "brief_description", "difficulty_level"]
        if not all(key in data for key in required_fields):
            return {"error": "Missing required fields"}
        
        # Validate difficulty level
        valid_difficulty_levels = ["Beginner", "Intermediate", "Advanced"]
        if data["difficulty_level"] not in valid_difficulty_levels:
            return {"error": "Invalid difficulty level. Must be one of: Beginner, Intermediate, Advanced"}
        
        # Validate title length
        if len(data["title"]) < 3 or len(data["title"]) > 100:
            return {"error": "Course title must be between 3 and 100 characters"}
        
        # Validate brief description length
        if len(data["brief_description"]) < 10 or len(data["brief_description"]) > 500:
            return {"error": "Brief description must be between 10 and 500 characters"}

        return CourseModel.create_course(data)

    @staticmethod
    def update_course(course_id, data):
        # First check if course exists
        existing_course = CourseModel.get_course_by_id(course_id)
        if not existing_course:
            return {"error": "Course not found"}

        # Validate required fields
        required_fields = ["title", "brief_description", "difficulty_level"]
        if not all(key in data for key in required_fields):
            return {"error": "Missing required fields"}
        
        # Validate difficulty level
        valid_difficulty_levels = ["Beginner", "Intermediate", "Advanced"]
        if data["difficulty_level"] not in valid_difficulty_levels:
            return {"error": "Invalid difficulty level. Must be one of: Beginner, Intermediate, Advanced"}
        
        # Validate title length
        if len(data["title"]) < 3 or len(data["title"]) > 100:
            return {"error": "Course title must be between 3 and 100 characters"}
        
        # Validate brief description length
        if len(data["brief_description"]) < 10 or len(data["brief_description"]) > 500:
            return {"error": "Brief description must be between 10 and 500 characters"}

        return CourseModel.update_course(course_id, data)

    @staticmethod
    def delete_course(course_id):
        if not course_id:
            return {"error": "Course ID is required"}
        
        # First check if course exists
        existing_course = CourseModel.get_course_by_id(course_id)
        if not existing_course:
            return {"error": "Course not found"}
        
        # Additional business logic could go here
        # For example, check if there are any students enrolled in the course
        # before allowing deletion
        
        return CourseModel.delete_course(course_id)
