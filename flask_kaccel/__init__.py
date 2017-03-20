__import__('pkg_resources').declare_namespace(__name__)
from flask import Response, request
from .mime import MIME
import os

try:
	from flask import _app_ctx_stack as stack
except ImportError:
	from flask import _request_ctx_stack as stack

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
	- KACCEL_BASE_PATH
	- KACCEL_BUFFER
	- KACCEL_CHARSET
	- KACCEL_CACHE_EXPIRES
	- KACCEL_LIMIT_RATE

    '''
	def __init__(self, app=None):
		self.app = app
		if app is not None:
			self.init_app(app)

	def init_app(self, app):
		config_host		= app.config.get('KACCEL_HOST')
		config_path 	= app.config.get('KACCEL_BASE_PATH')
		config_buffer 	= app.config.get('KACCEL_BUFFER')
		config_charset 	= app.config.get('KACCEL_CHARSET')
		config_expires 	= app.config.get('KACCEL_CACHE_EXPIRES')
		config_limit 	= app.config.get('KACCEL_LIMIT_RATE')
	
		if config_host:
			self.host = config_host
		else:
			self.host = request.host

		if config_path:
			self.redirect_path = config_path
		else:
			self.redirect_path = "/files/%s"

		if config_buffer:
			self.buffering = 'yes'
		else:
			self.buffering = 'no'

		if config_charset:
			self.charset = config_charset
		else:
			self.charset = "utf-8"

		if config_expires:
			self.cache_expires = config_expires
		else:
			self.cache_expires = 'off'

		if config_limit:
			self.limit_rate = config_limit
		else:
			self.limit_rate = 'off'

	def filesize(self, file):
		''' get file size in byte
		
		:param file: fullpath
		:return: return <integer> if success and False if failed.
		'''
		try:
			return os.path.getsize(file)
		except:
			return False

	def filename(self, file):
		''' get file name from full path.
		
		:param file: fullpath
		:return: return <string> if success and False if failed.
		'''
		try:
			return os.path.basename(file)
		except:
			return False

	def extension(self, file):
		''' get extension from full path.

		:param file: fullpath
		:return: return <string> if success and False if failed.
		'''
		try:
			name, ext = os.path.splitext(self.filename(file))
			return ext
		except:
			return False

	def mimetype(self, file):
		''' get mime type from file

		:param file: fullpath
		:return: return <string> if success and return "application/octet-stream" if mime type not found.
		'''
		try:
			ext  = self.extension(file)
			mime = MIME.get(ext)
			if not mime:
				mime = "application/octet-stream"
			return mime
		except:
			return "application/octet-stream"

	def send_file(self, file, redirect="/files/%s", buffering='yes', charset='utf-8', expires='off', limit='off'):
		''' send file from directory using custom configuration.

		:param file: fullpath.
		:param redirect: redirect path, default= "/files/%s"
		:param buffering: sets the proxy buffering for this connection, value= "yes" | "no"
		:param charset: sets the charset of the file, default= "utf-8"
		:param expires: sets when to expire the file in the internal NGINX cache, value= "off" | seconds
		:param limit: sets the rate limit for this single request. off means unlimited, value= "off" | bytes
		:return: return Request() object if success and False if failed.
		'''
		try:
			if self.host == request.host:
				return "Error: direct access is forbidden"

			content_length	= self.filesize(file)
			content_type 	= self.mimetype(file)
			filename		= self.filename(file)

			if not content_length or not content_type or not filename:
				return False

			resp = Response()
			resp.headers['Content-Length'] 		= content_length
			resp.headers['Content-Type'] 		= content_type
			resp.headers['Content-Disposition'] = "attachment; filename=%s" % (str(filename))
			resp.headers['X-Accel-Redirect'] 	= redirect % (str(filename))
			resp.headers['X-Accel-Buffering'] 	= buffering
			resp.headers['X-Accel-Charset'] 	= charset
			resp.headers['X-Accel-Expires'] 	= expires
			resp.headers['X-Accel-Limit-Rate'] 	= limit
			return resp
		
		except:
			return False

	def send_from_directory(self, file):
		''' send file from directory using global configuration.

		:param file: fullpath
		:return: return Request() object if success and False if failed.
		'''
		return self.send_file(file=file, redirect=self.redirect_path, buffering=self.buffering, charset=self.charset, expires=self.cache_expires, limit=self.limit_rate)