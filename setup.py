from setuptools import setup, find_packages

setup(
    name = "pantograph",
    version = "0.1.0",
    author = "Howard Mao",
    author_email = "zhehao.mao@gmail.com",
    description = "Python library for drawing on HTML5 canvas",
    url = "https://github.com/adicu/pantograph",
    license = "MIT",
    
    include_package_data = True,
    packages = find_packages(exclude=["example"]),
    install_requires = ["tornado>=2.2"]
)
