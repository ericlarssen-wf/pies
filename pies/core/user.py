import sqlalchemy as sa

import atlas


class User(atlas.Base):
    id = sa.Column(sa.String(50), primary_key=True)
    name = sa.Column(sa.String(50) nullable=True)
    last_login = sa.Column(sa.DateTime())
