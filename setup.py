from setuptools import setup, find_packages

setup(
    name='landingpermit_app', 
    version='0.1',  
    packages=find_packages(where='src'),  # Tells setuptools to find packages under src
    package_dir={'': 'src'},  # Tells setuptools that packages are under src
    install_requires=[
        'numpy',
        'pandas==2.0.3',
        'pendulum==2.1.2',
        'python-dateutil==2.8.2',
        'pytz==2023.3',
        'pytzdata==2020.1',
        'six==1.16.0',
        'tzdata==2023.3',
    ],
    include_package_data=True,  
)
