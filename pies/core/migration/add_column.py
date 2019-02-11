import sqlalchemy as sa


name = sa.Column('name', sa.String(50), nullable=True)


def get_user_table(metadata):
    return metadata.tables['user']


def up(metadata):
    user_table = get_user_table(metadata)

    user_table.create_column(name)
    user_table.update().values(name='freddie mercury')


def down(metadata):
    user_table = get_user_table(metadata)

    user_table.drop_column(name)
