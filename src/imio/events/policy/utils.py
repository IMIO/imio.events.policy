# -*- coding: utf-8 -*-

from plone import api
from plone.app.multilingual.browser.setup import SetupMultilingualSite
from plone.app.multilingual.subscriber import set_recursive_language
from zope.component.hooks import getSite

import logging

logger = logging.getLogger("imio.events.policy")


def remove_unused_contents(portal):
    api.content.delete(portal.news)
    api.content.delete(portal.events)
    api.content.delete(portal.Members)


def setup_multilingual_site(context):
    portal = api.portal.get()

    setup_tool = SetupMultilingualSite()
    setup_tool.setupSite(getSite())

    available_languages = api.portal.get_registry_record("plone.available_languages")
    fr_folder = getattr(portal, "fr")
    for brain in api.content.find(context=portal, depth=1):
        if brain.getId in available_languages:
            continue
        obj = brain.getObject()
        set_recursive_language(obj, "fr")
        api.content.move(obj, target=fr_folder)
        logger.info(f"Moved {brain.getId} content to 'fr' folder.")

    for brain in api.content.find(portal_type="LIF"):
        lif_id = brain.getId
        obj = brain.getObject()
        api.content.delete(obj)
        logger.info(f"Deleted LIF folder {lif_id}.")
