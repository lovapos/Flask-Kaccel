__import__('pkg_resources').declare_namespace(__name__)
from flask import Response, request, abort
from .mime import MIME
from .version import version
from os import path

class Kaccel(object):
	'''Class used to control the Kaccel integration to a Flask application.

	You can use this by providing the Flask app on instantiation or by calling
	an :meth:`init_app` method an instance object of `Kaccel`. Here an
	example of providing the application on instantiation: ::

		app = Flask(__name__)
		kaccel = Kaccel(app)

	And here calling the :meth:`init_app` method: ::

		kaccel = Kaccel()

		def init_app():
			app = Flask(__name__)
			kaccel.init_app(app)
			return app

	:Config:

	- KACCEL_HOST
	- KACCEL_REDIRECT_PATH
	- KACCEL_FILES_PATH
	- KACCEL_BUFFER
	- KACCEL_CHARSET
	- KACCEL_CACHE_EXPIRES
	- KACCEL_LIMIT_RATE

	'''
	def __init__(self, app=None):
		# Set
		self.app = app
		self.version = version

		# Init app
		if app:
			self.init_app(app)

	def init_app(self, app):
		# Get config
		config_host = app.config.get('KACCEL_HOST')
		config_redirect_path = app.config.get('KACCEL_REDIRECT_PATH')
		config_files_path = app.config.get('KACCEL_FILES_PATH')
		config_buffer = app.config.get('KACCEL_BUFFER')
		config_charset = app.config.get('KACCEL_CHARSET')
		config_expires = app.config.get('KACCEL_CACHE_EXPIRES')
		config_limit = app.config.get('KACCEL_LIMIT_RATE')
	
		# Set config
		self.host = config_host or request.host
		self.files_path = config_files_path or None
		self.redirect_path = config_redirect_path or None
		self.buffering = config_buffer or True
		self.charset = config_charset or "utf-8"
		self.cache_expires = config_expires or False
		self.limit_rate = config_limit or False

	def _bool(self, value):
		if value:
			return "yes"
		else:
			return "no"
	
	def _off(self, value):
		if not value:
			return "off"
		return value

	def filesize(self, file_path):
		''' get file size in byte
		
		:param file_path: fullpath
		:return: return <integer> if success and None if fail.
		'''
		try:
			return path.getsize(file_path)
		except:
			return None

	def filename(self, file_path):
		''' get file name from full path.
		
		:param file_path: fullpath
		:return: return <string> if success and None if fail.
		'''
		try:
			return path.basename(file_path)
		except:
			return None

	def extension(self, file_path):
		''' get extension from full path.

		:param file_path: fullpath
		:return: return <string> if success and None if fail.
		'''
		try:
			name, ext = path.splitext(self.filename(file_path))
			return ext
		except:
			return None

	def mimetype(self, file_path):
		''' get mime type from file

		:param file_path: fullpath
		:return: return <string> if success and return "application/octet-stream" if mime type not found.
		'''
		try:
			ext = self.extension(file_path)
			mime = MIME.get(ext)
			if not mime:
				mime = "application/octet-stream"
			return mime
		except:
			return "application/octet-stream"

	
	def send_from_directory(self, filename):
		''' send file from directory using global configuration.

		:param filename: file name
		:return: return Request() object if success and error 404 if fail.
		'''
		return self.send_file(
			file_path = path.join(self.files_path, filename),
			redirect = self.redirect_path,
			buffering = self.buffering,
			charset = self.charset,
			expires = self.cache_expires,
			limit = self.limit_rate
		)

	def send_file(
			self,
			file_path,
			redirect = None,
			buffering = True,
			charset = 'utf-8',
			expires = None,
			limit = None
		):
		''' send file from directory using custom configuration.

		:param file_path: fullpath.
		:param redirect: redirect path, default=None
		:param buffering: sets the proxy buffering for this connection, value=(True|False), default=True
		:param charset: sets the charset of the file, default="utf-8"
		:param expires: sets when to expire the file in the internal NGINX cache, value=(None|int), default=None
		:param limit: sets the rate limit for this single request. off means unlimited, value=(None|int), default=None
		:return: return Request() object if success and error 404 if fail.
		'''
		try:
			if self.host == request.host:
				return abort(404)

			content_length	= self.filesize(file_path)
			content_type 	= self.mimetype(file_path)
			filename		= self.filename(file_path)

			if not content_length or not content_type or not filename:
				return abort(404)

			response = Response()
			response.headers['Content-Length'] = content_length
			response.headers['Content-Type'] = content_type
			response.headers['Content-Disposition'] = "attachment; filename=%s" % (str(filename))
			response.headers['X-Accel-Redirect'] = path.join(redirect, filename)
			response.headers['X-Accel-Buffering'] = self._bool(buffering)
			response.headers['X-Accel-Charset'] = charset
			response.headers['X-Accel-Expires'] = self._off(expires)
			response.headers['X-Accel-Limit-Rate'] = self._off(limit)
			return response

		except:
			return abort(404)
