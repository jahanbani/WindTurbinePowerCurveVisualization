#!/usr/bin/env python3
import os
from app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    app.run_server(host="0.0.0.0", port=port, debug=False) 