from decimal import Decimal

from sqlalchemy import DECIMAL, CheckConstraint, Column, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()


wallets = Table(
    'finances_wallets', metadata,
    Column('id', Integer, primary_key=True),
    Column('label', String(32), index=True),
    Column('balance', DECIMAL(precision=65, scale=18), default=Decimal('0'), index=True),
    CheckConstraint('balance >= 0', name='wallet_balance_cant_be_negative'),
)

transactions = Table(
    'finances_transactions', metadata,
    Column('id', Integer, primary_key=True),
    Column(
        'wallet_id',
        Integer,
        ForeignKey(
            'finances_wallets.id',
            ondelete='RESTRICT'
        ),
        nullable=False
    ),
    Column('txid', String(36), unique=True, nullable=False),
    Column('amount', DECIMAL(precision=65, scale=18), index=True),
)
