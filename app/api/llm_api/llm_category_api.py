# -*- coding: utf-8 -*-
# @Time    : 2024/8/3 16:19
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : llm_category_api.py
# @Software: PyCharm

from all_reference import *
from app.models.admin.models import Admin
from app.models.llm.models import LLMCategory
from app.api.llm_api.common import query_llm_category

llm_category_router = APIRouter()


class CreateLLMCategoryReqData(CommonPydanticCreate):
    name: str = "LLM 分类"
    is_public: int = 1


class UpdateLLMCategoryReqData(CommonPydanticUpdate):
    name: str
    is_public: int


class DeleteLLMCategoryReqData(BaseModel):
    id: int


class LLMCategoryPage(CommonPage):
    name: str = "LLMCategory Name"
    creator_id: Union[int, None] = None


@llm_category_router.get("/{category_id}")
async def llm_category_detail(category_id: int, admin: Admin = Depends(check_admin_existence)):
    """LLM分类详情"""

    result, llm_category = await query_llm_category(category_id)
    if not result:
        return api_response(code=10002, message=f"LLM 分类 {category_id} 不存在")
    else:
        return api_response(data=jsonable_encoder(llm_category))


@llm_category_router.post("/")
async def create_llm_category(request_data: CreateLLMCategoryReqData, admin: Admin = Depends(check_admin_existence)):
    """新增 LLM 分类"""

    name = request_data.name
    query_llm_category = await LLMCategory.filter(name=name).first()
    if query_llm_category:
        return api_response(code=10003, message=f"LLM 分类 {name} 已存在")

    request_data.creator_id = admin.id
    request_data.creator = admin.username
    save_data = request_data.dict()
    new_llm_category = await LLMCategory.create(**save_data)
    return api_response(http_code=status.HTTP_201_CREATED, code=201, data=jsonable_encoder(new_llm_category))


@llm_category_router.put("/")
async def update_llm_category(request_data: UpdateLLMCategoryReqData, admin: Admin = Depends(check_admin_existence)):
    """编辑 LLM 分类"""

    llm_category_id = request_data.id
    llm_category = await LLMCategory.get_or_none(id=llm_category_id)
    if not llm_category:
        return api_response(code=10002, message=f"LLM 分类 {llm_category_id} 不存在")

    request_data.modifier_id = admin.id
    request_data.modifier = admin.username
    update_data = request_data.dict()
    del update_data["id"]
    await llm_category.update_from_dict(update_data).save()
    return api_response(data=jsonable_encoder(llm_category))


@llm_category_router.delete("/")
async def delete_llm_category(request_data: DeleteLLMCategoryReqData, admin: Admin = Depends(check_admin_existence)):
    """删除 LLM 分类"""

    llm_category_id = request_data.id
    llm_category = await LLMCategory.get_or_none(id=llm_category_id)
    if not llm_category:
        return api_response(code=10002, message=f"LLM 分类 {llm_category_id} 不存在")
    else:
        ud = {
            "is_deleted": llm_category_id,
            "modifier": admin.username,
            "modifier_id": admin.id,
        }
        await llm_category.update_from_dict(ud).save()
        return api_response()


@llm_category_router.post("/page")
async def llm_category_page(request_data: LLMCategoryPage, admin: Admin = Depends(check_admin_existence)):
    """LLM列表"""

    data = await cpq(
        request_data, LLMCategory,
        None,
        ["name"],
        ["creator_id"],
        ["-update_time"]
    )
    return api_response(data=data)
