from setuptools import setup, find_packages
from flask_kaccel.version import version

with open('README.md') as f:
	long_description = f.read()

setup(
	name='Flask-Kaccel',
	version=version,
	url='https://flask-kaccel.readthedocs.io/en/latest/',
	license='MIT',
	author='LovaPOS',
	author_email='dev@lovapos.com',
	description='Add Flask support for Nginx X-Accel',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=find_packages(include=['flask_kaccel']),
	namespace_packages=['flask_kaccel'],
	zip_safe=False,
	platforms='any',
	install_requires=[
		'Flask'
	],
	project_urls={
		'Documentation': 'https://flask-kaccel.readthedocs.io/en/latest/',
		'Source': 'https://github.com/lovapos/Flask-Kaccel',
	},
	keywords='flask nginx x-accel',
	python_requires='>=3',
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
		'Topic :: Software Development :: Libraries :: Python Modules',
	]
)
