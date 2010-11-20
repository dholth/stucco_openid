import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [ 
'pyramid',
'pyramid_beaker',
'pyramid_jinja2',
'python-openid',
'WebError',
]

setup(name='ponzi_openid',
      version='0.1',
      description='ponzi_openid',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: OSI Approved :: BSD License"
        ],
      author='Daniel Holth',
      author_email='dholth@fastmail.fm',
      url='http://bitbucket.org/dholth/ponzi_openid',
      keywords='web pyramid pylons openid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="ponzi_openid",
      entry_points = """\
      [paste.app_factory]
      main = ponzi_openid:main
      """,
      paster_plugins=['pyramid'],
      )

