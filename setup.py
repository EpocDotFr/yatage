# Original setup.py template: https://github.com/kennethreitz/setup.py

from shutil import rmtree
import io
import os
import sys

from setuptools import find_packages, setup, Command

NAME = 'yatage'
DESCRIPTION = 'Yet Another Text Adventure Game Engine'
URL = 'https://github.com/EpocDotFr/yatage'
EMAIL = 'contact.nospam@epoc.nospam.fr'
AUTHOR = 'Maxime "Epoc" G.'
REQUIRES_PYTHON = '>=3.8'
VERSION = None # See yatage/__version__.py

REQUIRED = [
    'pyyaml~=6.0',
]

EXTRAS = {
    'dev': {
        'wheel~=0.38',
        'Sphinx~=5.3',
        'twine~=4.0',
        'pytest~=7.2',
    }
}

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Topic :: Games/Entertainment',
]

PROJECT_URLS = {
    'Documentation': 'https://epocdotfr.github.io/yatage/',
    'Source': 'https://github.com/EpocDotFr/yatage',
    'Tracker': 'https://github.com/EpocDotFr/yatage/issues',
}

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

about = {}

if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")

    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='DBAD',
    entry_points={
        'console_scripts': [
            'yatage = yatage.cli:cli',
        ]
    },
    classifiers=CLASSIFIERS,
    cmdclass={
        'upload': UploadCommand,
    },
    project_urls=PROJECT_URLS
)
