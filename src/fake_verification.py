import secrets
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone


@dataclass
class VerificationChallenge:
    address: str
    code: str
    expires_at: datetime
    consumed: bool = False


@dataclass
class FakeVerificationService:
    ttl_seconds: int = 300
    challenges: dict[str, VerificationChallenge] = field(default_factory=dict)

    def issue_code(self, address: str) -> str:
        code = f"{secrets.randbelow(1_000_000):06d}"
        self.challenges[address] = VerificationChallenge(
            address=address,
            code=code,
            expires_at=datetime.now(timezone.utc) + timedelta(seconds=self.ttl_seconds),
        )
        return code

    def verify_code(self, address: str, code: str) -> bool:
        challenge = self.challenges.get(address)
        if not challenge or challenge.consumed:
            return False
        if datetime.now(timezone.utc) > challenge.expires_at:
            return False
        if not secrets.compare_digest(challenge.code, code):
            return False
        challenge.consumed = True
        return True
