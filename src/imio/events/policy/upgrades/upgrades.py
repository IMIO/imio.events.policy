# -*- coding: utf-8 -*-
from imio.events.policy.utils import install_omnia_tinymce as install_omnia_tiny
from plone import api

import logging

logger = logging.getLogger("imio.events.policy")
# PROFILEID = "profile-imio.events.policy:default"


def install_kimug(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runAllImportStepsFromProfile("profile-pas.plugins.kimug:default")


def install_omnia_tinymce(context):
    install_omnia_tiny()
