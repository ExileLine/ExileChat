# -*- coding: utf-8 -*-
# @Time    : 2024/8/3 16:57
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : secretary_category_api.py
# @Software: PyCharm

from all_reference import *
from app.models.admin.models import Admin
from app.models.secretary.models import SecretaryCategory
from app.api.secretary_api.common import query_secretary_category

secretary_category_router = APIRouter()


class CreateSecretaryCategoryReqData(CommonPydanticCreate):
    name: str = "助手分类"
    is_public: int = 1


class UpdateSecretaryCategoryReqData(CommonPydanticUpdate):
    name: str
    is_public: int


class DeleteSecretaryCategoryReqData(BaseModel):
    id: int


class SecretaryCategoryPage(CommonPage):
    name: str = "助手分类名称"
    creator_id: Union[int, None] = None


@secretary_category_router.get("/{category_id}")
async def secretary_category_detail(category_id: int, admin: Admin = Depends(check_admin_existence)):
    """助手分类详情"""

    result, secretary_category = await query_secretary_category(category_id)
    if not result:
        return api_response(code=10002, message=f"助手分类 {category_id} 不存在")
    else:
        return api_response(data=jsonable_encoder(secretary_category))


@secretary_category_router.post("/")
async def create_secretary_category(
        request_data: CreateSecretaryCategoryReqData,
        admin: Admin = Depends(check_admin_existence)
):
    """新增助手分类"""

    name = request_data.name
    query_secretary_category = await SecretaryCategory.filter(name=name).first()
    if query_secretary_category:
        return api_response(code=10003, message=f"助手分类 {name} 已存在")

    request_data.creator_id = admin.id
    request_data.creator = admin.username
    save_data = request_data.dict()
    new_secretary_category = await SecretaryCategory.create(**save_data)
    return api_response(http_code=status.HTTP_201_CREATED, code=201, data=jsonable_encoder(new_secretary_category))


@secretary_category_router.put("/")
async def update_secretary_category(
        request_data: UpdateSecretaryCategoryReqData,
        admin: Admin = Depends(check_admin_existence)
):
    """编辑助手分类"""

    secretary_category_id = request_data.id
    secretary_category = await SecretaryCategory.get_or_none(id=secretary_category_id)
    if not secretary_category:
        return api_response(code=10002, message=f"助手分类 {secretary_category_id} 不存在")

    request_data.modifier_id = admin.id
    request_data.modifier = admin.username
    update_data = request_data.dict()
    del update_data["id"]
    await secretary_category.update_from_dict(update_data).save()
    return api_response(data=jsonable_encoder(secretary_category))


@secretary_category_router.delete("/")
async def delete_secretary_category(
        request_data: DeleteSecretaryCategoryReqData,
        admin: Admin = Depends(check_admin_existence)
):
    """删除助手分类"""

    secretary_category_id = request_data.id
    secretary_category = await SecretaryCategory.get_or_none(id=secretary_category_id)
    if not secretary_category:
        return api_response(code=10002, message=f"助手分类 {secretary_category_id} 不存在")
    else:
        ud = {
            "is_deleted": secretary_category_id,
            "modifier": admin.username,
            "modifier_id": admin.id,
        }
        await secretary_category.update_from_dict(ud).save()
        return api_response()


@secretary_category_router.post("/page")
async def secretary_category_page(request_data: SecretaryCategoryPage, admin: Admin = Depends(check_admin_existence)):
    """助手列表"""

    data = await cpq(
        request_data, SecretaryCategory,
        None,
        ["name"],
        ["creator_id"],
        ["-update_time"]
    )
    return api_response(data=data)
