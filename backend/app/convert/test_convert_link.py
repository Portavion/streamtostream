from fastapi.testclient import TestClient

from .router import router
from .service import convert_link

client = TestClient(router)


def test_read_shared_link():
    response = client.get(
        "/convert-link/{link: path}?link=%2Ftidal.com%2Fbrowse%2Ftrack%2F126102208%3Fu"
    )
    assert response.status_code == 200
    assert response.json() == {"link": "/tidal.com/browse/track/126102208?u"}


def return_converted_links():
    converted_links = convert_link("/tidal.com/browse/track/126102208?u")
    assert (
        converted_links
        == "open.spotify.com/track/3tYxhPqkioZEV5el3DJxLQ?si=a9108519124545e0"
    )
