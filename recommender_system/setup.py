from setuptools import find_packages, setup

setup(
    name="recommender_system",
    packages=find_packages(exclude=["recommender_system_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
