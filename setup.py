import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.txt")).read()
CHANGES = open(os.path.join(here, "CHANGES.txt")).read()

requires = [
    "Akhet",
    "Babel",
    "SQLAHelper",
    "SQLAlchemy",
    "WebError",
    "pyramid>=1.0a10",
    "pyramid_beaker",
    "pyramid_handlers",
    "pyramid_tm",
    "transaction",
    "webhelpers",
    "zope.sqlalchemy",
]

if sys.version_info[:3] < (2,5,0):
   requires.append("pysqlite")


entry_points = """\
    [paste.app_factory]
    main = drkpr:main

    [paste.app_install]
    main = paste.script.appinstall:Installer
"""

setup(name="drkpr",
      version="0.0",
      description="drkpr",
      long_description=README + "\n\n" +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author="Dyno (Hongjun) Fu",
      author_email="dyno.fu@gmail.com",
      url="www.cpksecurity.com",
      keywords="web pyramid pylons",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="drkpr",
      entry_points=entry_points,
      paster_plugins=["pyramid"],
      #Babel
      package_data={'drkpr': ['locale/*/LC_MESSAGES/*.mo']},
      message_extractors={'drkpr': [
            ('**.py', 'python', None),
            ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
            ('static/**', 'ignore', None)]},
      )

