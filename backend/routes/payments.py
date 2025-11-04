from flask import Blueprint, request, jsonify
from db import execute_query, fetch_all, fetch_one
from utils.auth_middleware import token_required
import uuid
from datetime import datetime

payments_bp = Blueprint('payments', __name__)


@payments_bp.route('/create', methods=['POST'])
@token_required
def create_payment(current_user):
    data = request.get_json()
    subscription_id = data.get('subscription_id')
    amount = data.get('amount')
    payment_method = data.get('payment_method', 'Credit Card')
    payment_status = data.get('payment_status', 'Pending')

    if not (subscription_id and amount):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    # Verify the subscription belongs to the current user
    sub = fetch_one("SELECT Subscription_Id FROM subscription WHERE Subscription_Id = %s AND User_Id = %s", 
                    (subscription_id, current_user))
    if not sub:
        return jsonify({"success": False, "message": "Subscription not found or not owned by user"}), 403

    # Generate unique transaction ID
    transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"

    query = """
        INSERT INTO payment (Subscription_Id, Amount, Payment_Method, Payment_Status, Transaction_Id)
        VALUES (%s, %s, %s, %s, %s)
    """
    execute_query(query, (subscription_id, amount, payment_method, payment_status, transaction_id))
    return jsonify({"success": True, "message": "Payment recorded", "transaction_id": transaction_id})


@payments_bp.route('/subscription/<int:subscription_id>', methods=['GET'])
@token_required
def get_payments_for_subscription(current_user, subscription_id):
    # Verify subscription ownership
    sub = fetch_one("SELECT Subscription_Id FROM subscription WHERE Subscription_Id = %s AND User_Id = %s", 
                    (subscription_id, current_user))
    if not sub:
        return jsonify({"success": False, "message": "Subscription not found or not owned by user"}), 403

    rows = fetch_all("SELECT * FROM payment WHERE Subscription_Id = %s ORDER BY Payment_Date DESC", (subscription_id,))
    return jsonify({"success": True, "payments": rows})


@payments_bp.route('/history', methods=['GET'])
@token_required
def get_user_payment_history(current_user):
    query = """
        SELECT p.*, s.Start_Date, s.End_Date
        FROM payment p
        JOIN subscription s ON p.Subscription_Id = s.Subscription_Id
        WHERE s.User_Id = %s
        ORDER BY p.Payment_Date DESC
    """
    rows = fetch_all(query, (current_user,))
    return jsonify({"success": True, "payments": rows})
