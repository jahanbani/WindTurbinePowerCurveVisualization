#!/usr/bin/env python3
import os
import sys
from app import app

# Print information for debugging
print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("Current directory:", os.getcwd())
print("Directory contents:", os.listdir('.'))

if __name__ == "__main__":
    # Get port from environment variable
    port = int(os.environ.get("PORT", 4000))
    print(f"Starting server on port {port}")
    
    # Run app
    app.run_server(host="0.0.0.0", port=port, debug=False) 