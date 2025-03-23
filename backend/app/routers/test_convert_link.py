from fastapi.testclient import TestClient

from .convert_link import router

client = TestClient(router)


def test_read_shared_link():
    response = client.get(
        "/convert-link/{link: path}?link=%2Ftidal.com%2Fbrowse%2Ftrack%2F126102208%3Fu"
    )
    assert response.status_code == 200
    assert response.json() == {"link": "/tidal.com/browse/track/126102208?u"}
