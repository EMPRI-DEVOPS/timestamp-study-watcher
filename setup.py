from setuptools import setup, find_packages


with open('README.md') as f:
    README = f.read()

setup(
    name='sitewatcher',
    version='0.1.0',
    description='Watch site for changes in selected XPaths',
    long_description=README,
    long_description_content_type="text/markdown",
    maintainer='Christian Burkert',
    maintainer_email='cs@cburkert.de',
    license="BSD",
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'selenium',
    ],
    entry_points={
        'console_scripts': [
            'sitewatcher = sitewatcher.sitewatcher:main'
        ]
    },
)
