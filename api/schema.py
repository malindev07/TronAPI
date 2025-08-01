from pydantic import BaseModel


class WalletInfoSchema(BaseModel):
    address: str
    balance: float = 0.0
    bandwidth: int = 0
    energy: int = 0
