# Route/chat.py
from flask import Blueprint, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit
from datetime import datetime

# Blueprint
chat_bp = Blueprint("chat", __name__, template_folder="../templates")

# SocketIO
socketio = SocketIO(cors_allowed_origins="*")

# ========== Routes ==========
@chat_bp.route("/chat/student")
def chat_student():
    return render_template("chat_student.html")

@chat_bp.route("/chat/mentor")
def chat_mentor():
    return render_template("chat_mentor.html")

@chat_bp.route("/chat/group")
def chat_group():
    return render_template("chat_group.html")   # ✅ صفحة الجروب شات

# ========== Socket Events ==========
@socketio.on("connect")
def handle_connect():
    print("✅ Client connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("❌ Client disconnected")

# ----- One-to-One Chat -----
@socketio.on("join_chat")
def handle_join_chat(data):
    student_id = data["student_id"]
    mentor_id = data["mentor_id"]
    sender_id = data["sender_id"]

    room = f"{student_id}_{mentor_id}"
    join_room(room)

    emit("receive_message", {
        "sender_id": "System",
        "content": f"User {sender_id} joined the chat",
        "timestamp": datetime.now().strftime("%H:%M")
    }, room=room)

@socketio.on("leave_chat")
def handle_leave_chat(data):
    student_id = data["student_id"]
    mentor_id = data["mentor_id"]
    sender_id = data["sender_id"]

    room = f"{student_id}_{mentor_id}"
    leave_room(room)

    emit("receive_message", {
        "sender_id": "System",
        "content": f"User {sender_id} left the chat",
        "timestamp": datetime.now().strftime("%H:%M")
    }, room=room)

@socketio.on("send_message")
def handle_send_message(data):
    student_id = data["student_id"]
    mentor_id = data["mentor_id"]
    sender_id = data["sender_id"]
    content = data["content"]

    room = f"{student_id}_{mentor_id}"
    emit("receive_message", {
        "sender_id": sender_id,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M")
    }, room=room)


# ----- Group Chat -----
@socketio.on("join_group")
def handle_join_group(data):
    room = data["room_id"]
    sender_name = data["sender_name"]

    join_room(room)
    emit("receive_group_message", {
        "sender_id": "System",
        "content": f"{sender_name} joined the room",
        "timestamp": datetime.now().strftime("%H:%M")
    }, room=room)

@socketio.on("leave_group")
def handle_leave_group(data):
    room = data["room_id"]
    sender_name = data["sender_name"]

    leave_room(room)
    emit("receive_group_message", {
        "sender_id": "System",
        "content": f"{sender_name} left the room",
        "timestamp": datetime.now().strftime("%H:%M")
    }, room=room)

@socketio.on("send_group_message")
def handle_send_group_message(data):
    room = data["room_id"]
    emit("receive_group_message", {
        "sender_id": data["user_id"],
        "sender_name": data["sender_name"],
        "sender_type": data["user_type"],
        "content": data["content"],
        "timestamp": datetime.now().strftime("%H:%M")
    }, room=room)
