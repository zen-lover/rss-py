from requests import get

def test_statuscode():
    assert get('http://farsi.khamenei.ir/rss').status_code == 200
