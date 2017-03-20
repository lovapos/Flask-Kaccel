from setuptools import setup

setup(
    name='Flask-Kaccel',
    version='1.0',
    url='http://bapakode.org/flask-kaccel',
    license='MIT',
    author='Bapakode Open Source',
    author_email='opensource@bapakode.org',
    description='Add Flask support for Nginx X-Accel',
    packages=['flask_kaccel'],
    namespace_packages=['flask_kaccel'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
