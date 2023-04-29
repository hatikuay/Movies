from app import db, Movie

db.create_all()

mov1 = Movie(title="Hotel Rwanda", release_year=2004,
             director="Terry George", runtime=121)
mov2 = Movie(title="Yesterday", release_year=2004,
             director="Darrell Roodt", runtime=90)
mov3 = Movie(title="Invictus", release_year=2009,
             director="Clint Eastwood", runtime=134)
mov4 = Movie(title="Sarafina!", release_year=1992,
             director="Darrell Roodt", runtime=117)

db.session.add(mov1)
db.session.add(mov2)
db.session.add(mov3)
db.session.add(mov4)

db.session.commit()


