#!usr/bin/env python
# -*- coding:utf-8 _*-
import logging
from django.utils.translation import gettext_lazy as _


class BlueException(Exception):

    ERROR_CODE = "0000000"
    MESSAGE = _("APP异常")
    STATUS_CODE = 500
    LOG_LEVEL = logging.ERROR

    def __init__(self, message=None, data=None, *args):
        """
        :param message: 错误消息
        :param data: 其他数据
        :param context: 错误消息 format dict
        :param args: 其他参数
        """
        super(BlueException, self).__init__(*args)
        self.message = self.MESSAGE if message is None else message
        self.data = data

    def render_data(self):
        return self.data

    def response_data(self):
        return {
            "result": False,
            "code": self.ERROR_CODE,
            "message": self.message,
            "data": self.render_data(),
        }


class ServerBlueException(BlueException):

    MESSAGE = _("服务端服务异常")
    ERROR_CODE = "50000"
    STATUS_CODE = 500


class ApiNetworkError(ServerBlueException):

    MESSAGE = _("网络异常导致远程服务失效")
    ERROR_CODE = "50301"
    STATUS_CODE = 503


class ApiResultError(ServerBlueException):

    MESSAGE = _("远程服务请求结果异常")
    ERROR_CODE = "50302"
    STATUS_CODE = 503
