from pydantic import BaseModel


class WalletNotFoundSchema(BaseModel):
    address: str
    msg: str = "Not found"


class WalletInfoSchema(BaseModel):
    address: str
    balance: float = 0.0
    bandwidth: int = 0
    energy: int = 0
