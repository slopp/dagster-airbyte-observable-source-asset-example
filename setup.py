from setuptools import find_packages, setup

setup(
    name="dagster_proj",
    packages=find_packages(),
    package_data={"dagster_proj": ["../dbt_project/*", "../dbt_project/*/*"]},
    install_requires=[
        "dagster",
        "dagster-cloud",
        "boto3",
        "dagster-airbyte",
        "dagster-managed-elements",
        "dagster-dbt",
        "dagster-postgres",
        "pandas",
        "numpy",
        "scipy",
        "dbt-core",
        "dbt-postgres",
        "packaging<22.0",  # match dbt-core's requirement to workaround a resolution issue
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
