"""第15次课：用 Flask 测试客户端（test_client）做请求级测试

注意：路由以仓库实际为准——创建工单是 /tickets/new，详情是 /tickets/<id>。
"""


def test_index(client):
    """首页应返回 200 且包含 CampusFix 标题"""
    resp = client.get("/")
    assert resp.status_code == 200
    assert "CampusFix".encode("utf-8") in resp.data


def test_detail(client):
    """先建一条工单，再访问它的详情页"""
    client.post(
        "/tickets/new",
        data={"title": "详情页测试", "room": "A区101", "description": "灯坏了"},
    )
    resp = client.get("/tickets/1")
    assert resp.status_code == 200
    assert "详情页测试".encode("utf-8") in resp.data


def test_create(client):
    """提交表单后跟随跳转，列表页应出现新工单"""
    resp = client.post(
        "/tickets/new",
        data={"title": "测试工单", "room": "A区101", "description": "灯坏了"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert "测试工单".encode("utf-8") in resp.data
