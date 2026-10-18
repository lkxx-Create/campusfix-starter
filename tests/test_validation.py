"""第14-16次课：标题长度校验的单元测试 + 请求级测试 + 等价类/边界值测试"""
import pytest

from app import validate_ticket


def test_title_too_long():
    """21 个字符超过 20 字符上限，应返回错误提示"""
    error = validate_ticket("A" * 21, "A101")
    assert error == "标题不能超过20个字符"


def test_post_title_too_long(client):
    """请求级测试：超长标题通过真实 POST 提交应被 400 拒绝"""
    resp = client.post(
        "/tickets/new",
        data={"title": "A" * 21, "room": "A区101", "description": "测试"},
    )
    assert resp.status_code == 400
    assert "标题不能超过20个字符" in resp.data.decode("utf-8")


@pytest.mark.parametrize(
    "title,expected",
    [
        ("测试工单", 200),   # 有效类代表值（4 字符）
        ("A" * 19, 200),    # 边界内
        ("A" * 20, 200),    # 恰好等于上限
        ("A" * 21, 400),    # 越界（差一个）
        ("A" * 100, 400),   # 无效类代表值
    ],
    ids=["4chars", "19chars", "20chars", "21chars", "100chars"],
)
def test_title_boundary(client, title, expected):
    """等价类划分 + 边界值分析：成功用例会 302 跳转，故跟随重定向后看 200"""
    resp = client.post(
        "/tickets/new",
        data={"title": title, "room": "A区101", "description": "测试"},
        follow_redirects=True,
    )
    assert resp.status_code == expected


