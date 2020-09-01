from setuptools import setup

setup(
    name='Flask-Kaccel',
    version='1.0',
    url='https://flask-kaccel.readthedocs.io/en/latest/',
    license='MIT',
    author='LovaPOS',
    author_email='dev@lovapos.com',
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
