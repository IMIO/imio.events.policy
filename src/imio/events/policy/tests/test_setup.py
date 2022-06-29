# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from imio.events.policy.testing import IMIO_EVENTS_POLICY_INTEGRATION_TESTING
from imio.events.policy.utils import setup_multilingual_site
from plone import api
from plone.app.multilingual.api import is_translatable
from plone.app.testing import setRoles, TEST_USER_ID
from Products.CMFPlone.interfaces import ILanguage
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that imio.events.policy is properly installed."""

    layer = IMIO_EVENTS_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if imio.events.policy is installed."""
        self.assertTrue(self.installer.is_product_installed("imio.events.policy"))

    def test_browserlayer(self):
        """Test that IImioEventsPolicyLayer is registered."""
        from imio.events.policy.interfaces import IImioEventsPolicyLayer
        from plone.browserlayer import utils

        self.assertIn(IImioEventsPolicyLayer, utils.registered_layers())

    def test_multilingual(self):
        self.assertIn("fr", self.portal.objectIds())
        self.assertIn("nl", self.portal.objectIds())

        # no LIF folders
        self.assertEqual(len(self.portal.fr.objectIds()), 0)
        self.assertEqual(len(self.portal.nl.objectIds()), 0)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        entity = api.content.create(
            container=self.portal,
            type="imio.events.Entity",
            id="entity",
        )
        agenda = api.content.create(
            container=entity,
            type="imio.events.Agenda",
            id="agenda",
        )
        folder = api.content.create(
            container=agenda,
            type="imio.events.Folder",
            id="folder",
        )
        api.content.create(
            container=folder,
            type="imio.events.Event",
            id="event",
        )
        setup_multilingual_site(self.portal)
        self.assertNotIn("entity", self.portal.objectIds())
        self.assertIn("entity", self.portal.fr.objectIds())
        entity = self.portal.fr.entity
        self.assertIn("agenda", entity.objectIds())
        agenda = entity.agenda
        self.assertIn("folder", agenda.objectIds())
        folder = agenda.folder
        self.assertIn("event", folder.objectIds())
        event = folder.event
        self.assertTrue(is_translatable(event))
        self.assertEquals(ILanguage(event).get_language(), "fr")


class TestUninstall(unittest.TestCase):

    layer = IMIO_EVENTS_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("imio.events.policy")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if imio.events.policy is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("imio.events.policy"))

    def test_browserlayer_removed(self):
        """Test that IImioEventsPolicyLayer is removed."""
        from imio.events.policy.interfaces import IImioEventsPolicyLayer
        from plone.browserlayer import utils

        self.assertNotIn(IImioEventsPolicyLayer, utils.registered_layers())
