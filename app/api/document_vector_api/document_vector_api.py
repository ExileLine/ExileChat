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
from utils.ai.llm_engine import LLMEngine
from utils.ai.process_vector.process_vector import ProcessVector

document_router = APIRouter()

UPLOAD_DIR = os.getcwd() + "/app/static"


class GeneDocumentVectorReqData(CommonPydanticCreate):
    id: int


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

    from api_key import api_key
    llm_engine = LLMEngine(model_name='azure_open_ai', api_key=api_key)
    pv = ProcessVector(document=document, llm_engine=llm_engine)
    # await pv.main()
    background_tasks.add_task(pv.main)
    return api_response()
