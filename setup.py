from setuptools import setup, find_packages


def read_requirements():
    with open("requirements.txt", "r") as req:
        content = req.read()
        requirements = content.split('\n')
    return requirements


setup(
    name="stonks",
    version="0.6.0",
    author="dinghino",
    description="Data scraper and aggregator for the stock market",
    author_email="dinghino@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    # Commands are work in progress, they will later consolidated in one
    # The choice on launching the cli or not will depend on the arguments
    # provided.
    entry_points='''
        [console_scripts]
        stonks-cli=cli:launch
        stonk=launcher:main
    '''
)
