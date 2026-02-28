import os
import uuid
from dataclasses import dataclass

from flask import request
from injector import inject
from openai import OpenAI

from internal.exception import FailException
from internal.schema import CompletionReq
from internal.service.app_service import AppService
from pkg.response import success_json, validate_error_json


@inject
@dataclass
class AppHandler:
    """应用控制器"""
    app_service: AppService

    def create_app(self):
        app = self.app_service.create_app()
        return success_json(f"成功创建应用，id: {app.id}")

    def get_app(self, id: uuid.UUID):
        app = self.app_service.get_app(app_id=id)
        return success_json(f"成功获取应用： {app.name}")

    def update_app(self, id: uuid.UUID):
        app = self.app_service.update_app(app_id=id, name=request.json.get("name"))
        return success_json(f"成功更新应用：{app.name}")

    def delete_app(self, id: uuid.UUID):
        app = self.app_service.delete_app(app_id=id)
        return success_json(f"成功删除应用: {app.id}")

    def completion(self):
        """聊天机器人"""
        # 1.接受请求参数 POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(errors=req.errors)

        query = request.json.get("query")

        # 2. 创建 OpenAI客户端
        client = OpenAI(base_url=os.getenv("OPENAI_BASE_URL"), )

        response = client.chat.completions.create(
            model="MiniMax-M2.5",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query},
            ],
            # 设置 reasoning_split=True 将思考内容分离到 reasoning_details 字段
            extra_body={"reasoning_split": True},
        )
        content = response.choices[0].message.content
        return success_json(data={"content": content})

    def ping(self):
        raise FailException("测试异常")
        return {"ping": "pong"}
