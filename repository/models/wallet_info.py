import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from repository.models.base import Base


class WalletInfoModel(Base):
    __tablename__ = "wallet_info"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    address: Mapped[str] = mapped_column(nullable=False, unique=False)
    balance: Mapped[float] = mapped_column(nullable=False)
    bandwidth: Mapped[int] = mapped_column(nullable=False)
    energy: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
