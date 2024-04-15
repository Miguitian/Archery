#!usr/bin/env python
# -*- coding:utf-8 _*-
import logging

from django.conf import settings
from django.contrib import auth
from django.core.cache import caches
from django.http import HttpResponseRedirect

from blueapps.forms import AuthenticationForm

try:
    from django.utils.deprecation import MiddlewareMixin
except Exception:  # pylint: disable=broad-except
    MiddlewareMixin = object

logger = logging.getLogger('default')
cache = caches["default"]


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view, args, kwargs):
        form = AuthenticationForm(request.COOKIES)
        if form.is_valid():
            bk_token = form.cleaned_data["bk_token"]
            session_key = request.session.session_key
            if session_key:
                # 确认 cookie 中的 ticket 和 cache 中的是否一致
                cache_session = cache.get(session_key)
                is_match = cache_session and bk_token == cache_session.get("bk_token")
                if is_match and request.user.is_authenticated:
                    return None

            user = auth.authenticate(request=request, bk_token=bk_token)
            if user is not None and user.username != request.user.username:
                auth.login(request, user)

            if user is not None and request.user.is_authenticated:
                # 登录成功，重新调用自身函数，即可退出
                cache.set(
                    session_key, {"bk_token": bk_token}, settings.LOGIN_CACHE_EXPIRED
                )
                return self.process_view(request, view, args, kwargs)

        return HttpResponseRedirect(settings.BK_URL)

    def process_response(self, request, response):
        return response
