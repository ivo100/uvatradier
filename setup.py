from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setup(
	name='uvatradier',
	version='0.4.9',
	author='tom hammons',
	description='tradier python wrapper',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/thammo4/uvatradier',
	python_requires=">=3.10",
	packages=find_packages(),
	project_urls={'Bug Tracker':'https://github.com/thammo4/uvatradier/issues'},
	keywords='tradier finance api',
    install_requires=[
        'requests>=2.25',
		'python-dotenv>=1.0',
		'pandas>=2.0',
        'matplotlib>=3.5',
		"websockets>=10.3",
        'asyncio'  			# asyncio is included in the standard library for Python 3.7 and later - unneeded if using these versions.
    ]
)
