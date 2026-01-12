#!/usr/bin/env python3
"""
PantryPilot Web Interface
A Flask-based web UI for the Safeway API client
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from safeway_api import SafewayAPIClient, SafewayEndpoints
import os
import json

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        username = data.get('username')
        password = data.get('password')
        store_id = data.get('store_id')
        
        if not all([username, password, store_id]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Test authentication
        client = SafewayAPIClient(username, password, store_id)
        if client.authenticate():
            session['username'] = username
            session['password'] = password
            session['store_id'] = store_id
            return jsonify({'success': True, 'message': 'Logged in successfully'})
        else:
            return jsonify({'error': 'Authentication failed'}), 401
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    if not all(k in session for k in ['username', 'password', 'store_id']):
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', store_id=session.get('store_id'))


@app.route('/api/offers')
def api_offers():
    """Get all offers"""
    if not all(k in session for k in ['username', 'password', 'store_id']):
        return jsonify({'error': 'Not authenticated'}), 401
    
    client = SafewayAPIClient(
        session['username'],
        session['password'],
        session['store_id']
    )
    
    if not client.authenticate():
        return jsonify({'error': 'Authentication failed'}), 401
    
    manufacturer_coupons = client.get_manufacturer_coupons()
    personalized_offers = client.get_personalized_offers()
    shopping_list = client.get_shopping_list()
    
    return jsonify({
        'manufacturer_coupons': [
            {
                'id': c.coupon_id,
                'description': c.description,
                'type': c.offer_type
            }
            for c in manufacturer_coupons
        ],
        'personalized_offers': [
            {
                'id': o.offer_id,
                'name': o.name,
                'description': o.description,
                'type': o.offer_type
            }
            for o in personalized_offers
        ],
        'loaded_count': len(shopping_list)
    })


@app.route('/api/load-all', methods=['POST'])
def api_load_all():
    """Load all offers"""
    if not all(k in session for k in ['username', 'password', 'store_id']):
        return jsonify({'error': 'Not authenticated'}), 401
    
    client = SafewayAPIClient(
        session['username'],
        session['password'],
        session['store_id']
    )
    
    new_offers = client.load_all_offers()
    
    return jsonify({
        'success': True,
        'new_offers': new_offers,
        'message': f'Added {new_offers} new offers' if new_offers > 0 else 'No new offers'
    })


@app.route('/api/explore')
def api_explore():
    """Explore API endpoints"""
    if not all(k in session for k in ['username', 'password', 'store_id']):
        return jsonify({'error': 'Not authenticated'}), 401
    
    endpoint = request.args.get('endpoint', 'all')
    
    client = SafewayAPIClient(
        session['username'],
        session['password'],
        session['store_id']
    )
    
    results = client.explore_api(endpoint)
    
    return jsonify(results)


@app.route('/api/check-status')
def api_check_status():
    """Check API endpoint status"""
    import requests
    
    endpoints = {
        'oauth': SafewayEndpoints.OAUTH_TOKEN,
        'manufacturer_coupons': SafewayEndpoints.MANUFACTURER_COUPONS,
        'personalized_offers': SafewayEndpoints.PERSONALIZED_OFFERS,
        'shopping_list': SafewayEndpoints.SHOPPING_LIST,
    }
    
    status = {}
    
    for name, url in endpoints.items():
        try:
            response = requests.head(url, timeout=5)
            accessible = response.status_code in [200, 401, 403, 400]
            status[name] = {
                'accessible': accessible,
                'status_code': response.status_code
            }
        except Exception as e:
            status[name] = {
                'accessible': False,
                'error': str(e)
            }
    
    return jsonify(status)


@app.route('/explore')
def explore():
    """Explore page"""
    if not all(k in session for k in ['username', 'password', 'store_id']):
        return redirect(url_for('login'))
    
    return render_template('explore.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
