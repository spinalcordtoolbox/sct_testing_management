from setuptools import setup
import sct_dbtool


def parse_requirements(filename):
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


install_reqs = parse_requirements("requirements.txt")

setup(
    name='sct_dbtool',
    version=sct_dbtool.__version__,
    url='https://github.com/neuropoly',
    license='Apache License 2.0',
    author=sct_dbtool.__author__,
    author_email='christian.perone@gmail.com',
    description='A MRI database management tools.',
    long_description='A MRI database management tools.',
    packages=['sct_dbtool'],
    keywords='MRI, database, tool, management',
    platforms='Any',
    package_data={
      'sct_dbtool': ['static/*.*', 'templates/*.*'],
    },
    zip_safe=False,
    include_package_data=True,
    install_requires=install_reqs,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points={
        'console_scripts': [
            'sct_dbtool = sct_dbtool.main:run_main',
        ],
    },
)
