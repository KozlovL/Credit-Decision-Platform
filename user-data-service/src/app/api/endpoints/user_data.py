from fastapi import APIRouter

from app.constants import USER_DATA_PREFIX

router = APIRouter(prefix=USER_DATA_PREFIX)
