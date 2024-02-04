def test_healthz(client):

    resp = client.get("/healthz")
    assert resp.status_code == 200
