"""first_migration

Revision ID: bf53f17f5529
Revises:
Create Date: 2023-07-29 11:31:31.658505

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "bf53f17f5529"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "account",
        sa.Column("account_number", sa.String(length=22), nullable=False),
        sa.Column("account_name", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_account_number", "account", ["account_number"], unique=False)
    op.create_index(op.f("ix_account_email"), "account", ["email"], unique=True)
    op.create_index(op.f("ix_account_id"), "account", ["id"], unique=False)
    op.create_table(
        "transaction",
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=32, scale=2), nullable=False),
        sa.Column("transaction_date", sa.DateTime(), nullable=False),
        sa.Column("notified", sa.Boolean(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["account.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_id_account_id", "transaction", ["id", "account_id"], unique=False)
    op.create_index(op.f("ix_transaction_id"), "transaction", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_transaction_id"), table_name="transaction")
    op.drop_index("idx_id_account_id", table_name="transaction")
    op.drop_table("transaction")
    op.drop_index(op.f("ix_account_id"), table_name="account")
    op.drop_index(op.f("ix_account_email"), table_name="account")
    op.drop_index("idx_account_number", table_name="account")
    op.drop_table("account")
    # ### end Alembic commands ###