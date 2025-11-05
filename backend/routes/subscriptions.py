from flask import Blueprint, request, jsonify
from db import execute_query, fetch_all, fetch_one
from utils.auth_middleware import token_required
from datetime import datetime, timedelta

subscriptions_bp = Blueprint('subscriptions', __name__)

# Subscription plans
SUBSCRIPTION_PLANS = [
    {
        "id": 1,
        "name": "1 Month Plan",
        "duration_months": 1,
        "price": 0.00,
        "description": "Access all content for 1 month"
    },
    {
        "id": 2,
        "name": "3 Month Plan",
        "duration_months": 3,
        "price": 0.00,
        "description": "Access all content for 3 months"
    }
]


@subscriptions_bp.route('/plans', methods=['GET'])
def get_plans():
    """Get available subscription plans"""
    return jsonify({"success": True, "plans": SUBSCRIPTION_PLANS})


@subscriptions_bp.route('/subscribe', methods=['POST'])
@token_required
def subscribe(current_user):
    """Subscribe user to a plan"""
    data = request.get_json()
    plan_id = data.get('plan_id')
    
    if not plan_id:
        return jsonify({"success": False, "message": "plan_id is required"}), 400
    
    # Find the plan
    plan = next((p for p in SUBSCRIPTION_PLANS if p['id'] == plan_id), None)
    if not plan:
        return jsonify({"success": False, "message": "Invalid plan"}), 400
    
    # Calculate dates
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=30 * plan['duration_months'])
    
    # Create subscription
    query = """
        INSERT INTO subscription (User_Id, Start_Date, End_Date, Auto_Renewal, Payment_Status)
        VALUES (%s, %s, %s, %s, %s)
    """
    execute_query(query, (current_user, start_date, end_date, 0, 'Completed'))
    
    return jsonify({
        "success": True, 
        "message": f"Subscribed to {plan['name']} successfully!",
        "start_date": str(start_date),
        "end_date": str(end_date)
    })


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
	# Transform date objects to strings
	subscriptions = []
	for row in rows:
		sub = dict(row)
		if sub.get('Start_Date'):
			sub['Start_Date'] = str(sub['Start_Date'])
		if sub.get('End_Date'):
			sub['End_Date'] = str(sub['End_Date'])
		subscriptions.append(sub)
	return jsonify({"success": True, "subscriptions": subscriptions})


@subscriptions_bp.route('/status', methods=['GET'])
@token_required
def subscription_status(current_user):
	"""Get subscription status using database function"""
	row = fetch_one("SELECT fn_GetSubscriptionStatus(%s) AS status", (current_user,))
	status = row['status'] if row else 'None'
	
	# Get latest subscription details
	latest_sub = fetch_one(
		"SELECT * FROM subscription WHERE User_Id = %s ORDER BY Start_Date DESC LIMIT 1",
		(current_user,)
	)
	
	result = {
		"success": True,
		"status": status,
		"subscription": None
	}
	
	if latest_sub:
		result["subscription"] = {
			"start_date": str(latest_sub['Start_Date']) if latest_sub.get('Start_Date') else None,
			"end_date": str(latest_sub['End_Date']) if latest_sub.get('End_Date') else None,
			"auto_renewal": bool(latest_sub.get('Auto_Renewal')),
			"payment_status": latest_sub.get('Payment_Status')
		}
	
	return jsonify(result)
