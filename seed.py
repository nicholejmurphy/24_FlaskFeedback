from models import User, Feedback, db
from app import app

db.drop_all()
db.create_all()

Feedback.query.delete()
User.query.delete()

u1 = User(username='user1', password='user1', email='user1@mail.com',
          first_name='user1', last_name='userLast')
u2 = User(username='user2', password='user2', email='user2@mail.com',
          first_name='user2', last_name='userLast')
u3 = User(username='user3', password='user3', email='user3@mail.com',
          first_name='user3', last_name='userLast')
u4 = User(username='user4', password='user4', email='user4@mail.com',
          first_name='user4', last_name='userLast')
u5 = User(username='user5', password='user5', email='user5@mail.com',
          first_name='user5', last_name='userLast')

db.session.add_all([u1, u2, u3, u4, u5])
db.session.commit()

f1 = Feedback(title='Amazing', content='Things are Amazing!', username='user1')
f2 = Feedback(title='Pretty good',
              content='Things are Pretty good!', username='user2')
f3 = Feedback(title='Going okay',
              content='Things are Going okay!', username='user3')
f4 = Feedback(title='Could be better',
              content='Things could be better!', username='user4')
f5 = Feedback(title='Terrible',
              content='Things are Terrible!', username='user5')
f6 = Feedback(title="COULDN'T BE WORSE",
              content="Things COULDN'T BE WORSE!", username='user1')

db.session.add_all([f1, f2, f3, f4, f5, f6])
db.session.commit()
