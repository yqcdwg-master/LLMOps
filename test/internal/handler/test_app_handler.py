import json

import pytest


class TestAppHandler:
    """应用处理器单元测试"""

    def test_completion_success(self, client, mock_openai_response):
        """测试 completion 成功场景"""
        response = client.post(
            "/app/completion",
            data=json.dumps({"query": "你好"}),
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["code"] == "success"
        assert "content" in data["data"]

    @pytest.mark.parametrize(
        "query",
        [
            None,  # 缺少参数
            "",  # 空字符串
            "a" * 2001,  # 超出最大长度
        ],
        ids=["missing_query", "empty_query", "query_too_long"],
    )
    def test_completion_validation_error(self, client, query):
        """测试 completion 参数验证失败场景"""
        payload = {"query": query} if query is not None else {}
        response = client.post(
            "/app/completion",
            data=json.dumps(payload),
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["code"] == "validate_error"

    def test_ping(self, client):
        """测试 ping 接口抛出 FailException"""
        response = client.get("/ping")

        assert response.status_code == 200
        data = response.get_json()
        assert data["code"] == "fail"
        assert data["message"] == "测试异常"
