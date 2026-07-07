# -*- coding: utf-8 -*-

from plone import api


def remove_unused_contents(portal):
    api.content.delete(portal.news)
    api.content.delete(portal.events)
    api.content.delete(portal.Members)


def install_omnia_tinymce():
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runAllImportStepsFromProfile("profile-imio.omnia.tinymce:default")
