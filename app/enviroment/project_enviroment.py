import os
from enum import Enum


class Environment(Enum):
    STAGING = "staging"
    PRODUCTION = "production"


class ProjectEnvironment:

    def __init__(self, env: Environment):
        if not isinstance(env, Environment):
            raise ValueError("Invalid environment. Must be an instance of Environment Enum.")
        self.env = env

    def __str__(self):
        return f"ProjectEnvironment: {self.env.value.capitalize()}"

    def db_url(self) -> str:
        prod_database_url = os.environ.get('PROD_DATABASE_URL')
        staging_database_url = os.environ.get('STAGING_DATABASE_URL')

        if self.env == Environment.PRODUCTION:
            return prod_database_url

        elif self.env == Environment.STAGING:
            return staging_database_url
        else:
            raise ValueError("Unsupported environment.")
