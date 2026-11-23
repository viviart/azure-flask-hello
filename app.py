import os
import requests
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    url = os.environ.get('BLOB_SAS_URL')
    if not url:
        return 'Storage URL is not configured.', 500
    try:
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()
        data = response.raw.read(4097)
        response.close()
        if len(data) > 4096:
            return 'The sample file is too large.', 400
        message = data.decode('utf-8-sig')
        return render_template_string(
            '<h1>Storage lab</h1><p>Blob message: {{ message }}</p>',
            message=message,
        )
    except Exception:
        # Never log or display the URL, SAS, or exception details.
        return 'Storage read failed. Check configuration and network.', 503
