#!usr/bin/env python
# -*- coding:utf-8 _*-
from django import forms


class AuthenticationForm(forms.Form):
    bk_token = forms.CharField()
