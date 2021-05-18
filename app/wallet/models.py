from sqlalchemy import DateTime, Column, Integer, String, Table, ForeignKey, Numeric, func
from sqlalchemy import MetaData

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("username", String(50), unique=True),
    Column("created", DateTime, default=func.current_timestamp()),
    Column("updated", DateTime, default=func.current_timestamp(),
           onupdate=func.current_timestamp()),
)

wallets = Table(
    "wallets",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("owner_id", Integer, ForeignKey('users.id'), nullable=False, unique=True),
    Column("balance", Numeric(12, 2), default=0, nullable=False),
    Column("created", DateTime, default=func.current_timestamp()),
    Column("updated", DateTime, default=func.current_timestamp(),
           onupdate=func.current_timestamp()),
)

transfers = Table(
    "transfers",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("src_id", Integer, ForeignKey('wallets.id'), nullable=False),
    Column("dest_id", Integer, ForeignKey('wallets.id'), nullable=False),
    Column("amount", Numeric(12, 2), nullable=False),
    Column("created", DateTime, default=func.current_timestamp()),
)

deposits = Table(
    "deposits",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("wallet_id", Integer, ForeignKey('wallets.id'), nullable=False),
    Column("amount", Numeric(12, 2), nullable=False),
    Column("created", DateTime, default=func.current_timestamp()),
)
