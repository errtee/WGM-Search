from setuptools import setup, find_packages

setup(
        name='WGM-Search',
        version='0.1',
        author='Sascha Schneider',
        author_email='development@suntsu.org',
        url='https://github.com/SunTsu/WGM-Search',
        description='Simple web frontend that allows searching an exported CiviCRM database for wirgehenmit.org',
        long_description=__doc__,
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'setuptools',
            'Flask>=0.9',
            'Flask-WTF>=0.8.2',
            'pyGeoDb>=1.2',
            'Flask-SQLAlchemy>=0.16',
            'SQLAlchemy>=0.8.0b2',
            'WTForms>=1.0.2',
            'flup>=1.0.3.dev-20110405',
        ]
)

