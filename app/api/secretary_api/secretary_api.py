# -*- coding: utf-8 -*-
# @Time    : 2024/7/24 21:27
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : secretary_api.py
# @Software: PyCharm


from all_reference import *
from app.models.admin.models import Admin
from app.models.secretary.models import Secretary
from app.api.secretary_api.common import query_secretary_category, query_llm, query_able_list, AnswerMode

secretary_router = APIRouter()


class CreateSecretaryReqData(CommonPydanticCreate):
    category_id: int = 1
    cover: str = "https://www.metatuple.com/assets/img/favicon.png"
    name: str = "新增助手"
    introduce: str = "助手介绍"
    definition: str = "强大的人工智能"
    llm_id: int
    plugins_option: list[dict]
    quick_question: list[str]
    answer_mode: AnswerMode
    able_list: list[int]
    is_public: int = 1


class UpdateSecretaryReqData(CommonPydanticUpdate):
    category_id: int
    cover: str
    name: str
    introduce: str
    definition: str
    llm_id: int
    plugins_option: list[dict]
    quick_question: list[str]
    answer_mode: AnswerMode
    able_list: list[int]
    is_public: int


class DeleteSecretaryReqData(BaseModel):
    id: int


class SecretaryPage(CommonPage):
    category_id: Union[int, None] = None
    name: str = "Secretary Name"
    creator_id: Union[int, None] = None


@secretary_router.get("/{secretary_id}")
async def secretary_detail(secretary_id: int, admin: Admin = Depends(check_admin_existence)):
    """助手详情"""

    secretary = await Secretary.get_or_none(id=secretary_id)
    if not secretary:
        return api_response(code=10002, message=f"助手 {secretary_id} 不存在")
    else:
        category = None
        llm = None
        able_list = []

        result, secretary_category = await query_secretary_category(secretary.category_id)
        if result:
            category = jsonable_encoder(secretary_category)

        llm_result, secretary_llm = await query_llm(secretary.llm_id)
        if llm_result:
            llm = jsonable_encoder(secretary_llm)

        able_list_result, secretary_able_list = await query_able_list(secretary.able_list)
        if able_list_result:
            able_list = jsonable_encoder(secretary_able_list)

        data = jsonable_encoder(secretary)
        data["category"] = category
        data["llm"] = llm
        data["able_list"] = able_list
        return api_response(data=data)


@secretary_router.post("/")
async def create_secretary(request_data: CreateSecretaryReqData, admin: Admin = Depends(check_admin_existence)):
    """新增助手"""

    name = request_data.name
    category_id = request_data.category_id
    llm_id = request_data.llm_id
    able_list = request_data.able_list

    query_secretary = await Secretary.filter(name=name).first()
    if query_secretary:
        return api_response(code=10003, message=f"助手 {name} 已存在")

    sc_result, secretary_category = await query_secretary_category(category_id=category_id)
    if not sc_result:
        return api_response(code=10002, message=f"助手分类 {category_id} 不存在")

    llm_result, llm = await query_llm(llm_id=llm_id)
    if not llm_result:
        return api_response(code=10002, message=f"模型 {llm_id} 不存在")

    able_list_result, secretary_able_list = await query_able_list(ids=able_list)
    if not able_list_result:
        return api_response(code=10002, message=f"能力 {able_list} 不存在")

    request_data.creator_id = admin.id
    request_data.creator = admin.username
    save_data = request_data.dict()
    new_secretary = await Secretary.create(**save_data)
    return api_response(http_code=status.HTTP_201_CREATED, code=201, data=jsonable_encoder(new_secretary))


@secretary_router.put("/")
async def update_secretary(request_data: UpdateSecretaryReqData, admin: Admin = Depends(check_admin_existence)):
    """编辑助手"""

    secretary_id = request_data.id
    category_id = request_data.category_id
    llm_id = request_data.llm_id
    able_list = request_data.able_list

    secretary = await Secretary.get_or_none(id=secretary_id)
    if not secretary:
        return api_response(code=10002, message=f"助手 {secretary_id} 不存在")

    sc_result, secretary_category = await query_secretary_category(category_id)
    if not sc_result:
        return api_response(code=10002, message=f"助手分类 {category_id} 不存在")

    llm_result, llm = await query_llm(llm_id=llm_id)
    if not llm_result:
        return api_response(code=10002, message=f"模型 {llm_id} 不存在")

    able_list_result, secretary_able_list = await query_able_list(ids=able_list)
    if not able_list_result:
        return api_response(code=10002, message=f"能力 {able_list} 不存在")

    request_data.modifier_id = admin.id
    request_data.modifier = admin.username
    update_data = request_data.dict()
    del update_data["id"]
    await secretary.update_from_dict(update_data).save()
    return api_response(data=jsonable_encoder(secretary))


@secretary_router.delete("/")
async def delete_secretary(request_data: DeleteSecretaryReqData, admin: Admin = Depends(check_admin_existence)):
    """删除助手"""

    secretary_id = request_data.id
    secretary = await Secretary.get_or_none(id=secretary_id)
    if not secretary:
        return api_response(code=10002, message=f"助手 {secretary_id} 不存在")
    else:
        ud = {
            "is_deleted": secretary_id,
            "modifier": admin.username,
            "modifier_id": admin.id,
        }
        await secretary.update_from_dict(ud).save()
        return api_response()


@secretary_router.post("/page")
async def secretary_page(request_data: SecretaryPage, admin: Admin = Depends(check_admin_existence)):
    """助手列表"""

    data = await cpq(
        request_data, Secretary,
        None,
        ["name"],
        ["category_id", "creator_id"],
        ["-update_time"]
    )
    return api_response(data=data)
