import os
from config import db
from models import Movie, Director

# Data to initialize database with

DIRECTORS = [
    {'name': 'Simon Kinberg', 'gender': 2, 'uid': 1867384, 'department': 'Directing'},
    {'name': 'Cate Shortland', 'gender': 1, 'uid': 1867385, 'department': 'Directing'},
    {'name': 'Vicky Jewson', 'gender': 2, 'uid': 1867386, 'department': 'Directing'}
]

MOVIES = [
    {'original_title': 'Invasion', 'budget': 368009472, 'popularity': 103, 'release_date': '2021-03-09', 'revenue': 67490293, 'title': 'Invasion', 'vote_average': 7.2, 'vote_count': 4793, 'overview': 'Events unfold in real time through the eyes of five ordinary people across the globe as they struggle to make sense of the chaos unraveling around them', 'tagline': 'Hold on to your humanity', 'uid': 459489, 'director_id': 1},
    {'original_title': 'Venom', 'budget': 948039263, 'popularity': 157, 'release_date': '2021-01-10', 'revenue': 1928304836, 'title': 'Let There Be Carnage', 'vote_average': 9.3, 'vote_count': 5802, 'overview': 'After finding a host body in investigative reporter Eddie Brock, the alien symbiote must face a new enemy, Carnage, the alter ego of serial killer Cletus Kasady', 'tagline': 'Time to die', 'uid': 459490, 'director_id': 2},
    {'original_title': 'A hard day', 'budget': 273940835, 'popularity': 98, 'release_date': '2017-06-11', 'revenue': 389402784, 'title': 'A Hard Day', 'vote_average': 7.8, 'vote_count': 4805, 'overview': 'After trying to cover up a car accident that left a man dead, a crooked homicide detective is stalked by a mysterious man claiming to have witnessed the event', 'tagline': 'Witnessed it all', 'uid': 459491, 'director_id': 3}
]

# Delete database file if it exists currently
if os.path.exists('final_proj.db'):
    os.remove('final_proj.db')

# Create the database
db.create_all()

# Iterate over the PEOPLE structure and populate the database
for director in DIRECTORS:
    d = Director(name=director['name'], gender=director['gender'], uid=director['uid'], department=director['department'])
    db.session.add(d)

for movie in MOVIES:
    m = Movie(original_title=movie['original_title'], budget=movie['budget'], popularity=movie['popularity'], release_date=movie['release_date'], revenue=movie['revenue'], title=movie['title'], vote_average=movie['vote_average'], vote_count=movie['vote_count'], overview=movie['overview'], tagline=movie['tagline'], uid=movie['uid'], director_id=movie['director_id'])
    db.session.add(m)

db.session.commit()