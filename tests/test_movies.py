import pytest
from app import connex_app

@pytest.fixture(scope='module')
def client():
    with connex_app.app.test_client() as c:
        yield c

def test_post_movie_title(client):
    """
    Test that json response of key:original_title from /api/directors/{director_id}/movies is equals with expected data
    :param client:          Client of the app
    :return:                assertion and checking of json response of key:original_title
    """
    post_data = {
        "original_title": "Gonna Do It",
        "budget": 0,
        "popularity": 8,
        "release_date": "2019-09-04",
        "revenue": 374893028,
        "title": "Gonna Do It",
        "vote_average": 7.8,
        "vote_count": 82,
        "overview": "Kenny would do all things to make her family happy",
        "tagline": "Off Course, Gonna Do It",    
        "uid": 333
        }
    director_id = 6096
    response = client.post(f'/api/directors/{director_id}/movies', json=post_data)
    assert response.json.get('original_title') == 'Gonna Do It'

def test_post_movie_statmessage_badrequest(client):
    """
    Test that status response from /api/directors/{director_id}/movies is equals 
    with '400 BAD REQUEST' if some attribute is assigned with wrong data type
    :param client:          Client of the app
    :return:                assertion and checking of status response
    """
    post_data = post_data = {
        "original_title": "Eternals",
        "budget": "275371026",
        "popularity": 158,
        "release_date": "2020-03-11",
        "revenue":473820937,
        "title": "Eternals",
        "vote_average": "9.2",
        "vote_count": 473,
        "overview": "The Eternals secretly lived on Earth for thousands of years, reunite to battle the evil Deviants",
        "tagline": "A race of immortal beings",    
        "uid": "333"
        }
    director_id = 5174
    response = client.post(f'/api/directors/{director_id}/movies', json=post_data)
    assert response.status == '400 BAD REQUEST'