from outpost.django.base.key_constructors import (
    DetailKeyConstructor,
    ListKeyConstructor,
    PermissionKeyBit,
)


class PermissionDetailKeyConstructor(DetailKeyConstructor):
    permission = PermissionKeyBit()


class PermissionListKeyConstructor(ListKeyConstructor):
    permission = PermissionKeyBit()
