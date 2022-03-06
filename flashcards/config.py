from __future__ import annotations

import urllib.parse
from dataclasses import dataclass


@dataclass(frozen=True)
class PostgresConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

    @classmethod
    def from_uri(cls, uri: str) -> PostgresConfig:
        parsed_uri = urllib.parse.urlparse(uri)
        return cls(
            host=parsed_uri.hostname or '',
            port=parsed_uri.port or 0,
            user=parsed_uri.username or '',
            password=parsed_uri.password or '',
            database=parsed_uri.path.lstrip('/'),
        )

    def to_dsn(self) -> str:
        return (
            f'dbname={self.database} '
            f'user={self.user} '
            f'password={self.password} '
            f'host={self.host} '
            f'port={self.port}'
        )
