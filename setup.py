from setuptools import setup, find_packages

def read_requirements():
    with open("requirements.txt", "r") as req:
        content = req.read()
        requirements = content.split('\n')
    return requirements

setup(
    name="stocks",
    version="1.2",
    author="dinghino",
    author_email="my@email.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_poins='''
        [console_scripts]
        stocks=cli.cli:main
    '''
)
