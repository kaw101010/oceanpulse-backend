#!/usr/bin/env python3
"""
OceanPulse Backend - Main Entry Point

This is the main entry point for the OceanPulse backend application.
It imports and runs the Flask application defined in app.py.
"""

from app import app

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True, port=5000)