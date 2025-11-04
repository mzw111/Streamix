from flask import Blueprint, request, jsonify
from db import execute_query, fetch_all, fetch_one
from utils.auth_middleware import token_required

subscriptions_bp = Blueprint('subscriptions', __name__)


@subscriptions_bp.route('/create', methods=['POST'])
@token_required
def create_subscription(current_user):
	data = request.get_json()
	start_date = data.get('start_date')  # YYYY-MM-DD
	end_date = data.get('end_date')      # YYYY-MM-DD or null
	auto_renewal = data.get('auto_renewal', True)
	payment_status = data.get('payment_status', 'Pending')

	if not start_date:
		return jsonify({"success": False, "message": "start_date is required"}), 400

	query = """
		INSERT INTO subscription (User_Id, Start_Date, End_Date, Auto_Renewal, Payment_Status)
		VALUES (%s, %s, %s, %s, %s)
	"""
	execute_query(query, (current_user, start_date, end_date, int(bool(auto_renewal)), payment_status))
	return jsonify({"success": True, "message": "Subscription created"})


@subscriptions_bp.route('/list', methods=['GET'])
@token_required
def list_subscriptions(current_user):
	rows = fetch_all("SELECT * FROM subscription WHERE User_Id = %s ORDER BY Start_Date DESC", (current_user,))
	return jsonify({"success": True, "subscriptions": rows})


@subscriptions_bp.route('/status', methods=['GET'])
@token_required
def subscription_status(current_user):
	row = fetch_one("SELECT fn_GetSubscriptionStatus(%s) AS status", (current_user,))
	status = row['status'] if row else 'None'
	return jsonify({"success": True, "status": status})
