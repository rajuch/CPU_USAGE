'''Application setup file. Builds and installs the application.

@created: Mar 24, 2014
@author: Anshu Kumar, <anshu.choubey@imaginea.com>
'''

from setuptools import setup, find_packages

setup(
    name = "CPU USAGE",
    version = "0.1",
    packages = ['app'],
    install_requires = ['psutil>=2.0.0'],
    
    # Metadata.
    author = "Anshu Kumar",
    author_email = "anshu.choubey@imaginea.com",
    description = "This is a Webapp to display CPU usage on system.",
)