from setuptools import setup, find_packages


def read_requirements():
    with open("requirements.txt", "r") as req:
        content = req.read()
        requirements = content.split('\n')
    return requirements


setup(
    name="stonks",
    version="0.5.2",
    author="dinghino",
    description="Data scraper and aggregator for the stock market",
    author_email="dinghino@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points='''
        [console_scripts]
        stonks=cli.cli:start
    '''
)
