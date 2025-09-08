from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, CheckConstraint

metadata_obj = MetaData()

users = Table(
    'users',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('username', String, nullable=False),
    Column('name', String, nullable=False),
)

tasks = Table(
    'tasks',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('author_id', Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column('title', String, nullable=False),
    Column('description', String, nullable=False),
    Column('status', String(50), nullable=False, server_default='in-progress'),
    CheckConstraint("status in ('in-progress', 'done', 'failed')"),
)



