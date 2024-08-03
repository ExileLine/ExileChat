# -*- coding: utf-8 -*-
# @Time    : 2024/8/3 15:58
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : llm_api.py
# @Software: PyCharm


from all_reference import *
from app.models.admin.models import Admin
from app.models.llm.models import LLM
from app.api.llm_api.common import query_llm_category

llm_router = APIRouter()


class CreateLLMReqData(CommonPydanticCreate):
    category_id: int = 1
    name: str = "LLM"
    api_key: str = "api_key"
    options: list[dict]
    is_public: int = 1


class UpdateLLMReqData(CommonPydanticUpdate):
    category_id: int
    name: str
    api_key: str
    options: list[dict]
    is_public: int


class DeleteLLMReqData(BaseModel):
    id: int


class LLMPage(CommonPage):
    category_id: Union[int, None] = None
    name: str = "LLM Name"
    creator_id: Union[int, None] = None


@llm_router.get("/{llm_id}")
async def llm_detail(llm_id: int, admin: Admin = Depends(check_admin_existence)):
    """LLM详情"""

    llm = await LLM.get_or_none(id=llm_id)
    if not llm:
        return api_response(code=10002, message=f"LLM {llm_id} 不存在")
    else:
        result, llm_category = await query_llm_category(llm.category_id)
        if result:
            category = jsonable_encoder(llm_category)
        else:
            category = None
        data = jsonable_encoder(llm)
        data["category"] = category
        return api_response(data=data)


@llm_router.post("/")
async def create_llm(request_data: CreateLLMReqData, admin: Admin = Depends(check_admin_existence)):
    """新增 LLM"""

    name = request_data.name
    category_id = request_data.category_id

    query_llm = await LLM.filter(name=name).first()
    if query_llm:
        return api_response(code=10003, message=f"LLM {name} 已存在")

    result, llm_category = await query_llm_category(category_id)
    if not result:
        return api_response(code=10002, message=f"LLM 分类 {category_id} 不存在")

    request_data.creator_id = admin.id
    request_data.creator = admin.username
    save_data = request_data.dict()
    new_llm = await LLM.create(**save_data)
    return api_response(http_code=status.HTTP_201_CREATED, code=201, data=jsonable_encoder(new_llm))


@llm_router.put("/")
async def update_llm(request_data: UpdateLLMReqData, admin: Admin = Depends(check_admin_existence)):
    """编辑 LLM"""

    llm_id = request_data.id
    category_id = request_data.category_id

    llm = await LLM.get_or_none(id=llm_id)
    if not llm:
        return api_response(code=10002, message=f"LLM {llm_id} 不存在")

    result, llm_category = await query_llm_category(category_id)
    if not result:
        return api_response(code=10002, message=f"LLM 分类 {category_id} 不存在")

    request_data.modifier_id = admin.id
    request_data.modifier = admin.username
    update_data = request_data.dict()
    del update_data["id"]
    await llm.update_from_dict(update_data).save()
    return api_response(data=jsonable_encoder(llm))


@llm_router.delete("/")
async def delete_llm(request_data: DeleteLLMReqData, admin: Admin = Depends(check_admin_existence)):
    """删除 LLM"""

    llm_id = request_data.id
    llm = await LLM.get_or_none(id=llm_id)
    if not llm:
        return api_response(code=10002, message=f"LLM {llm_id} 不存在")
    else:
        ud = {
            "is_deleted": llm_id,
            "modifier": admin.username,
            "modifier_id": admin.id,
        }
        await llm.update_from_dict(ud).save()
        return api_response()


@llm_router.post("/page")
async def llm_page(request_data: LLMPage, admin: Admin = Depends(check_admin_existence)):
    """LLM列表"""

    data = await cpq(
        request_data, LLM,
        None,
        ["name"],
        ["category_id", "creator_id"],
        ["-update_time"]
    )
    return api_response(data=data)
