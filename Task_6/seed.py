from flask_script import Manager
from app import app, db
from dbmodels import Case
import datetime

manager = Manager(app)

# seed_data = [{}, {}]

@manager.command
def seed():
  print("Seeding the database...")

  try:
    case = Case(
      case_number = 'case number 1',
      open_date = datetime.datetime.today(),
      is_closed = True,
      close_date = datetime.datetime.today(),
      country = 'UK',
      service = 'Child Protection',
      case_text = 'Testing'
    )

    db.session.add(case)
    db.session.commit()

    print("Database seeded!")

  except Exception as e:
      return(str(e))


if __name__ == "__main__":
  manager.run()
