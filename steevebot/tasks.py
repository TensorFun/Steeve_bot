from __future__ import absolute_import, unicode_literals
from celery import task

from .model_cmd import *


@task
def periodic_crawler():
    steeve_crawler("Backend")