#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
author: Miguitian
@time: 2024/4/15
@description:
"""
import logging
import traceback

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from blueapps.utils.http import send

logger = logging.getLogger("default")

ROLE_TYPE_ADMIN = "1"


class TokenBackend(ModelBackend):
    def authenticate(self, request=None, bk_token=None):
        logger.debug(u"Enter in TokenBackend")
        # 判断是否传入验证所需的bk_token,没传入则返回None
        if not bk_token:
            return None

        verify_result, username = self.verify_bk_token(bk_token)
        # 判断bk_token是否验证通过,不通过则返回None
        if not verify_result:
            return None

        user_model = get_user_model()
        try:
            user, _ = user_model.objects.get_or_create(username=username)
            return user

        except IntegrityError:
            logger.exception(traceback.format_exc())
            logger.exception(
                u"get_or_create UserModel fail or update_or_create UserProperty"
            )
            return None
        except Exception:  # pylint: disable=broad-except
            logger.exception(traceback.format_exc())
            logger.exception(u"Auto create & update UserModel fail")
            return None

    @staticmethod
    def verify_bk_token(bk_token):
        """
        请求VERIFY_URL,认证bk_token是否正确
        @param bk_token: "_FrcQiMNevOD05f8AY0tCynWmubZbWz86HslzmOqnhk"
        @type bk_token: str
        @return: False,None True,username
        @rtype: bool,None/str
        """
        api_params = {"bk_token": bk_token}

        try:
            response = send(settings.BK_URL + "/login/accounts/is_login/", "GET", api_params, verify=False)
        except Exception:  # pylint: disable=broad-except
            logger.exception(u"Abnormal error in verify_bk_token...")
            return False, None

        if response.get("result"):
            data = response.get("data")
            username = data.get("username")
            return True, username
        else:
            error_msg = response.get("message", "")
            error_data = response.get("data", "")
            logger.error(
                u"Fail to verify bk_token, error={}, ret={}".format(
                    error_msg, error_data
                )
            )
            return False, None
