from dataclasses import dataclass


@dataclass
class User:
    username: str
    password: str


# ideally we would put the creds in environment variables
StandardUser = User("standard_user", "secret_sauce")
