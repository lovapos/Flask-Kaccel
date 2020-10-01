from flask import Flask, abort
from flask_kaccel import Kaccel
from os import path

app = Flask(__name__)
app.config.update(
		DEBUG = True,
		SECRET_KEY = 'test',
		# Kaccel
		KACCEL_HOST = "localhost:8080",
		KACCEL_BASE_PATH = "/files/%s" ,
		KACCEL_BUFFER = True,
		KACCEL_CHARSET = "utf-8",
		KACCEL_CACHE_EXPIRES = 60 * 60, # set expires time 1 minute
		KACCEL_LIMIT_RATE = 1024 * 64, # set download limit to 64kbps
)

# Initialize Kaccel
kaccel = Kaccel()
kaccel.init_app(app)

# Add Routes
@app.route('/download/<path:filename>')
def download(filename):
	return kaccel.send_from_directory(
			file = path.join("/var/www/files/", filename)
		)

# Error Handle
@app.errorhandler(404)
def not_found(error):
	return "Not Found", 404

if __name__ == "__main__":
		app.run(host='0.0.0.0', port=8080, debug=True)