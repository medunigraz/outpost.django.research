from appconf import AppConf
from django.conf import settings


class ResearchAppConf(AppConf):
    DSN = "FODOK-NEW"

    class Meta:
        prefix = "research"
