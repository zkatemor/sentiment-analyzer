from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


from db import session
from models.dictionary import Dictionary, Word

admin = Admin(name='Sentiment dashboard', template_mode='bootstrap3')

admin.add_view(ModelView(Dictionary, session.session))
admin.add_view(ModelView(Word, session.session))

