from app import app

def test_index_has_ticket():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert "工单" in resp.data.decode()