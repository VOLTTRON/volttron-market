from setuptools import setup, find_packages


#get environ for agent name/identifier
packages = find_packages('.')
package = packages[-1]

setup(
    name = "market",
    version = "0.1",
    install_requires = ['volttron'],
    packages = packages,
    namespace_packages = ['pnnl'],
    zip_safe = False
)