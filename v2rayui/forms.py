from django import forms
from django.conf import settings


class LoginForm(forms.Form):
    username = forms.CharField(required=True,
                               error_messages={"required": "请输入用户名"},
                               widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "用户名"})
                               )
    password = forms.CharField(required=True,
                               error_messages={"required": u"请输入密码"},
                               widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "密码", "type": "password"})
                               )


class RegisterForm(forms.Form):
    invite_code = forms.CharField(required=True,
                                  error_messages={"required": "请输入邀请码"},
                                  widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "邀请码，需要邀请码才可注册"})
                                  )
    username = forms.CharField(required=True,
                               error_messages={"required": "请输入用户名"},
                               widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "用户名"})
                               )
    password = forms.CharField(required=True,
                               error_messages={"required": u"请输入密码"},
                               widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "密码", "type": "password"})
                               )


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(required=True,
                                   error_messages={"required": u"请输入原密码"},
                                   widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入原密码", "type": "password"})
                                   )
    new_password = forms.CharField(required=True,
                                   error_messages={"required": u"请输入新密码"},
                                   widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入新密码", "type": "password"})
                                   )


class InviteCodeForm(forms.Form):
    invite_code_mark = forms.CharField(required=True,
                                       error_messages={"required": "请输入邀请码备注"},
                                       widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "邀请码备注"})
                                       )
    is_free = forms.ChoiceField(required=False,
                                choices=((True, "Yes"), (False, "No")),
                                widget=forms.Select(attrs={"class": "custom-select"})
                                )
    user_level = forms.IntegerField(required=False,
                                    widget=forms.NumberInput(attrs={"class": "form-control", "value": settings.DEFAULT_LEVEL}))
    user_expired_at = forms.DateTimeField(required=False,
                                          widget=forms.DateTimeInput(attrs={"class": "form-control", "placeholder": "日期格式：2020-01-01"}))


class ServerNodeForm(forms.Form):
    node_name = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "节点名称"})
                                )
    server_addr = forms.CharField(required=True,
                                  widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "节点IP或域名"})
                                  )
    server_port = forms.IntegerField(required=True,
                                     widget=forms.NumberInput(attrs={"class": "form-control", "value": 443}))
    protocol = forms.ChoiceField(required=True,
                                 choices=(("ws", "WebSocket"), ('http', "HTTP2")),
                                 widget=forms.Select(attrs={"class": "custom-select"})
                                 )
    path = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "URL路径"})
                           )
    is_enable = forms.ChoiceField(required=True,
                                  choices=((True, "Yes"), (False, "No")),
                                  widget=forms.Select(attrs={"class": "custom-select"})
                                  )
    country = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "节点的区域代码"})
                              )
    total_traffic = forms.IntegerField(required=False,
                                       widget=forms.NumberInput(attrs={"class": "form-control"}))
    comment = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "节点备注"})
                              )


class UserEditForm(forms.Form):
    user_id = forms.CharField(required=True,
                              widget=forms.HiddenInput()
                              )
    expire_at = forms.DateTimeField(required=False,
                                    widget=forms.DateTimeInput(attrs={"class": "form-control", "placeholder": "日期格式：2020-01-01"}))
    total_traffic = forms.IntegerField(required=False,
                                       widget=forms.NumberInput(attrs={"class": "form-control"}))
    invite_code_num = forms.IntegerField(required=False,
                                         widget=forms.NumberInput(attrs={"class": "form-control"}))
    is_free = forms.ChoiceField(required=False,
                                choices=((False, "No"), (True, "Yes")),
                                widget=forms.Select(attrs={"class": "custom-select"})
                                )
    level = forms.IntegerField(required=False,
                               widget=forms.NumberInput(attrs={"class": "form-control"}))
    alter_id = forms.IntegerField(required=False,
                                  widget=forms.NumberInput(attrs={"class": "form-control"}))
    password = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "请输入新密码, 不更改时请留空"})
                               )
