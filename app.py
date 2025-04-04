from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime
from urllib.parse import quote_plus
from gemini import generate
from shipping import load_fragmented_lanes, get_deterministic_lane, flatten_lane, get_lanes_yearly

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Serve the main page
@app.route('/')
def index():
    return "Hello world!"


@app.route('/data/<species>', methods=['GET'])
def get_species_data(species):
    try:
        # Call the OBIS API with the species name
        response = requests.get(f"https://api.obis.org/v3/occurrence/points/", params={'scientificname': species})
        response.raise_for_status()  # Raise an error for bad responses
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/data/<species>/<int:month>/<int:yr>', methods=['GET'])
def get_species_data_by_date(species, month, yr):
    try:
        # Calculate start and end dates
        start_date = datetime(yr, month, 1).strftime('%Y-%m-%d')
        end_date = datetime(yr, month + 1, 1).strftime('%Y-%m-%d') if month < 12 else datetime(yr + 1, 1, 1).strftime('%Y-%m-%d')
        
        # Call the OBIS API with the species name and date range
        response = requests.get(
            f"https://api.obis.org/v3/occurrence/points",
            params={
                'scientificname': species,
                'startdate': start_date,
                'enddate': end_date
            }
        )
        response.raise_for_status()  # Raise an error for bad responses
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/data/<species>/<int:yr>', methods=['GET'])
def get_species_data_for_year(species, yr):
    try:
        # Calculate start and end dates for the entire year
        start_date = datetime(yr, 1, 1).strftime('%Y-%m-%d')
        end_date = datetime(yr + 1, 1, 1).strftime('%Y-%m-%d')
        
        # Call the OBIS API with the species name and year range
        response = requests.get(
            f"https://api.obis.org/v3/occurrence/points",
            params={
                'scientificname': species,
                'startdate': start_date,
                'enddate': end_date
            }
        )
        response.raise_for_status()  # Raise an error for bad responses
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/data/shipping/<int:month>/<int:year>', methods=['GET'])
def get_shipping_lane(year, month):
    try:
        fragmented_lanes = load_fragmented_lanes("fragmented-utils/data/fragmented_shipping_lanes.json")

        selected_lane = get_deterministic_lane(fragmented_lanes, year, month)
        flattened = flatten_lane(selected_lane)

        return jsonify({
            'status': '1',
            'lane': flattened
        }), 200
    except Exception as e:
        return jsonify({'status': '-1', 'message': str(e)}), 500



@app.route('/data/shipping/<int:year>', methods=['GET'])
def get_annual_shipping_lanes(year):
    try:
        fragmented_lanes = load_fragmented_lanes("fragmented-utils/data/fragmented_shipping_lanes.json")

        selected_lane = get_lanes_yearly(fragmented_lanes, year)
        flattened = flatten_lane(selected_lane)

        return jsonify({
            'status': '1',
            'lane': flattened
        }), 200
    except Exception as e:
        return jsonify({'status': '-1', 'message': str(e)}), 500


@app.route('/generate', methods=['POST'])
def generate_content():
    try:
        # Get the prompt from the request JSON
        data = request.get_json()
        prompt = data.get('prompt', '')

        if not prompt:
            return jsonify({'status': '-1', 'message': 'Prompt is required'}), 400

        # Call the generate function with the prompt
        content = generate(prompt)
        return jsonify({'status': '1', 'content': content}), 200
    except Exception as e:
        return jsonify({'status': '-1', 'message': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'status': '-1',
        'message': 'Resource not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': '0',
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)