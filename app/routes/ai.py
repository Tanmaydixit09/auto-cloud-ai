from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

from app import db, limiter
from app.models import ChatMessage

ai_bp = Blueprint("ai", __name__)


@ai_bp.get("/ai-assistant")
@login_required
def assistant():
    messages = ChatMessage.query.filter_by(user_id=current_user.id).order_by(ChatMessage.created_at).all()
    return render_template("ai_assistant.html", messages=messages, active_page="ai")


@ai_bp.post("/api/ai/chat")
@login_required
@limiter.limit("10 per minute")
def chat():
    payload = request.get_json(silent=True) or {}
    prompt = str(payload.get("message", "")).strip()
    if not prompt or len(prompt) > 4000:
        return jsonify({"error": "Message must contain 1 to 4000 characters."}), 400
    user_message = ChatMessage(user_id=current_user.id, role="user", content=prompt)
    db.session.add(user_message)
    response = (
        "AI is not configured yet. Add GEMINI_API_KEY to your environment to enable "
        "cloud guidance. Your message was saved locally."
    )
    db.session.add(ChatMessage(user_id=current_user.id, role="assistant", content=response))
    db.session.commit()
    return jsonify({"reply": response})


@ai_bp.post("/api/ai/clear")
@login_required
def clear_chat():
    ChatMessage.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({"status": "cleared"})

