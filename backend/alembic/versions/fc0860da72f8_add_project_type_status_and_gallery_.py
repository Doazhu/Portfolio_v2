"""add_project_type_status_and_gallery_images

Revision ID: fc0860da72f8
Revises: 
Create Date: 2025-12-19 02:25:54.202382

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'fc0860da72f8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def table_exists(table_name: str) -> bool:
    """Check if a table exists in the database."""
    bind = op.get_bind()
    inspector = inspect(bind)
    return table_name in inspector.get_table_names()


def column_exists(table_name: str, column_name: str) -> bool:
    """Check if a column exists in a table."""
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns


def upgrade() -> None:
    # Create gallery_images table if it doesn't exist
    if not table_exists('gallery_images'):
        op.create_table('gallery_images',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('image_url', sa.String(length=500), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('likes', sa.Integer(), nullable=True, default=0),
            sa.Column('project_id', sa.Integer(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
            sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index('ix_gallery_images_id', 'gallery_images', ['id'], unique=False)

    # Add new columns to projects table if they don't exist
    with op.batch_alter_table('projects', schema=None) as batch_op:
        if not column_exists('projects', 'project_type'):
            batch_op.add_column(sa.Column('project_type', sa.String(length=20), nullable=True, server_default='external'))
        if not column_exists('projects', 'static_content'):
            batch_op.add_column(sa.Column('static_content', sa.Text(), nullable=True))
        if not column_exists('projects', 'static_path'):
            batch_op.add_column(sa.Column('static_path', sa.String(length=500), nullable=True))
        if not column_exists('projects', 'status'):
            batch_op.add_column(sa.Column('status', sa.String(length=20), nullable=True, server_default='draft'))


def downgrade() -> None:
    # Remove columns from projects table
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.drop_column('status')
        batch_op.drop_column('static_path')
        batch_op.drop_column('static_content')
        batch_op.drop_column('project_type')

    # Drop gallery_images table
    op.drop_index('ix_gallery_images_id', table_name='gallery_images')
    op.drop_table('gallery_images')
