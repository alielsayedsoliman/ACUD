from Model.mentorship import MentorshipModel

def request_mentor(studentID, mentorID):
    student = MentorshipModel.get_student(studentID)
    mentor = MentorshipModel.get_mentor(mentorID)

    if not student or not mentor:
        return {"error": "Student or Mentor not found"}, 404

    result = MentorshipModel.create_mentorship(studentID, mentorID)
    
    if isinstance(result, dict):
        if "error" in result:
            return {"error": result["error"]}, 500
        elif result["status"] == "exists":
            return {
                "message": f"Mentorship already exists between {student['name']} and {mentor['name']}",
                "status": "exists"
            }, 200
        else:
            return {
                "message": f"Mentorship created: {student['name']} -> {mentor['name']}",
                "status": "created"
            }, 201

    return {"error": "Unknown error occurred"}, 500

def get_assigned_students(mentorID):
    mentor = MentorshipModel.get_mentor(mentorID)
    if not mentor:
        return {"error": "Mentor not found"}, 404

    students = [
        {"userID": m.student.userID, "name": m.student.name}
        for m in mentor.mentorships
    ]

    return {"mentor": mentor.name, "students": students}, 200
