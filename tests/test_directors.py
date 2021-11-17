import pytest
from app import connex_app

@pytest.fixture(scope='module')
def client():
    with connex_app.app.test_client() as c:
        yield c

def test_read_director_statcode(client):
    """
    Test that status code response from /api/directors/{director_id} is 200
    :param client:          Client of the app
    :return:                assertion and checking of status code response
    """
    director_id = 4917
    response = client.get(f'/api/directors/{director_id}')
    assert response.status_code == 200

def test_read_director_json(client):
    """
    Test that json response from /api/directors/{director_id} is equals with expected data
    :param client:          Client of the app
    :return:                assertion and checking of json response
    """
    expected_data = {
        "department": "Directing",
        "gender": 2,
        "id": 5003,
        "movies": [
            {
                "budget": 80000000,
                "director_id": 5003,
                "id": 44049,
                "original_title": "Space Jam",
                "overview": "In a desperate attempt to win a basketball match and earn their freedom, the Looney Tunes seek the aid of retired basketball champion, Michael Jordan.",
                "popularity": 36,
                "release_date": "1996-11-15",
                "revenue": 250200000,
                "tagline": "Get ready to jam.",
                "title": "Space Jam",
                "uid": 2300,
                "vote_average": 6.5,
                "vote_count": 1288
            }
            ],
        "name": "Joe Pytka",
        "uid": 23677
        }
        
    director_id = 5003
    response = client.get(f'/api/directors/{director_id}')
    assert response.json == expected_data
