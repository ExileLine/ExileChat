# -*- coding: utf-8 -*-
# @Time    : 2024/7/28 21:16
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : document_vector_api.py
# @Software: PyCharm

import os

from all_reference import *
from app.models.admin.models import Admin
from app.models.able.models import Able
from app.models.document.models import Document
from app.models.llm.models import LLM
from aigc.llm_engine.llm_engine import LLMEngine
from aigc.llm_chat.llm_chat import AigcChat
from aigc.llm_embedding.llm_embedding import AigcEmbedding
from aigc.rag.process_vector import ProcessVector
from config.config import get_config

project_config = get_config()

document_router = APIRouter()

UPLOAD_DIR = os.getcwd() + "/app/static"


class GeneDocumentVectorReqData(CommonPydanticCreate):
    id: int
    llm_id: int
    able_id: int


@document_router.post("/upload")
async def upload_document(
        file: UploadFile = File(...),
        able_id: str | int = Form(...),
        admin: Admin = Depends(check_admin_existence)
):
    """上传文档"""

    able = await Able.get_or_none(id=able_id)
    if not able:
        return api_response(code=10002, message=f"能力 {able_id} 不存在")

    filename = file.filename
    file_ext = os.path.splitext(filename)[1].lower()
    save_path = UPLOAD_DIR + f"/{filename}"

    with open(save_path, "wb") as f:
        f.write(await file.read())

    save_data = {
        "able_id": able_id,
        "name": filename,
        "doc_suffix": file_ext,
        "doc_path": save_path,
        "handle_status": "ready",
        "creator_id": admin.id,
        "creator": admin.username
    }
    new_document = await Document.create(**save_data)

    return api_response(
        http_code=status.HTTP_201_CREATED,
        code=201,
        message=f"文档: {file.filename} 上传成功",
        data=jsonable_encoder(new_document)
    )


@document_router.post("/vector")
async def gene_document_vector(
        request_data: GeneDocumentVectorReqData,
        background_tasks: BackgroundTasks,
        admin: Admin = Depends(check_admin_existence),
):
    """生成文档向量"""

    document_id = request_data.id
    document = await Document.get_or_none(id=document_id)
    if not document:
        return api_response(code=10002, message=f"文档 {document_id} 不存在")

    llm_id = request_data.llm_id
    llm_example = await LLM.get_or_none(id=llm_id)
    if not llm_example:
        return api_response(code=10002, message=f"模型 {llm_id} 不存在")

    # engine = LLMEngine(
    #     company=llm_example.company,
    #     api_key=llm_example.api_key,
    #     client_options=llm_example.client_options
    # )

    # `engine`测试代码
    from api_key import api_key, azure_endpoint
    engine = LLMEngine(
        company='azure_open_ai',
        api_key=api_key,
        client_options={
            "api_version": "2024-02-01",
            "azure_endpoint": azure_endpoint
        }
    )
    aigc_chat = AigcChat(client=engine.client, model="gpt4o")
    aigc_embedding = AigcEmbedding(client=engine.client, model="embedding002")

    pv = ProcessVector(
        document=document,
        aigc_chat=aigc_chat,
        aigc_embedding=aigc_embedding,
        is_debug=project_config.DEBUG
    )
    background_tasks.add_task(pv.main)
    return api_response()
