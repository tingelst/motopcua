from setuptools import setup

package_name = "motopcua"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],
    install_requires=[
        "setuptools",
        "moto@git+https://github.com/tingelst/moto#egg=moto-0.0.1",
        "asyncua",
    ],
    zip_safe=True,
    maintainer="Lars Tingelstad",
    maintainer_email="lars.tingelstad@ntnu.no",
    description="",
    license="LGPL-3.0 License",
    tests_require=["pytest"],
    entry_points={"console_scripts": ["motopcua_server = motopcua.server:main"],},
)
