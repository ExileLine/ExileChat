# -*- coding: utf-8 -*-
# @Time    : 2024/7/24 21:26
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : able_api.py
# @Software: PyCharm

from all_reference import *
from app.models.admin.models import Admin
from app.models.able.models import Able

able_router = APIRouter()


class CreateAbleReqData(CommonPydanticCreate):
    able_category_id: int = 0
    cover: str = "https://www.metatuple.com/assets/img/favicon.png"
    name: str = "Able Name"
    introduce: str = "介绍"
    vector_llm_id: int = 0
    is_public: int = 1


class UpdateAbleReqData(CommonPydanticUpdate):
    able_category_id: int
    cover: str = "https://www.metatuple.com/assets/img/favicon.png"
    name: str
    introduce: str
    vector_llm_id: int
    is_public: int


class DeleteAbleReqData(BaseModel):
    id: int


class AblePage(CommonPage):
    name: str = "Able Name"
    creator_id: Union[int, None] = None


@able_router.get("/{able_id}")
async def able_detail(able_id: int, admin: Admin = Depends(check_admin_existence)):
    """能力详情"""

    able = await Able.get_or_none(id=able_id)
    if not able:
        return api_response(code=10002, message=f"数据 {able_id} 不存在")
    else:
        return api_response(data=jsonable_encoder(able))


@able_router.post("/")
async def create_able(request_data: CreateAbleReqData, admin: Admin = Depends(check_admin_existence)):
    """新增Able"""

    name = request_data.name
    query_able = await Able.filter(name=name).first()
    if query_able:
        return api_response(code=10003, message=f"数据 {name} 已存在")

    request_data.creator_id = admin.id
    request_data.creator = admin.username
    save_data = request_data.dict()
    new_able = await Able.create(**save_data)
    return api_response(http_code=status.HTTP_201_CREATED, code=201, data=jsonable_encoder(new_able))


@able_router.put("/")
async def update_able(request_data: UpdateAbleReqData, admin: Admin = Depends(check_admin_existence)):
    """更新Able"""

    able_id = request_data.id
    able = await Able.get_or_none(id=able_id)
    if not able:
        return api_response(code=10002, message=f"数据 {able_id} 不存在")

    request_data.modifier_id = admin.id
    request_data.modifier = admin.username
    update_data = request_data.dict()
    del update_data["id"]
    await able.update_from_dict(update_data).save()
    return api_response(data=jsonable_encoder(able))


@able_router.delete("/")
async def delete_able(request_data: DeleteAbleReqData, admin: Admin = Depends(check_admin_existence)):
    """删除Able"""

    able_id = request_data.id
    able = await Able.get_or_none(id=able_id)
    if not able:
        return api_response(code=10002, message=f"数据 {able_id} 不存在")
    else:
        ud = {
            "is_deleted": able_id,
            "modifier": admin.username,
            "modifier_id": admin.id,
        }
        await able.update_from_dict(ud).save()
        return api_response()
