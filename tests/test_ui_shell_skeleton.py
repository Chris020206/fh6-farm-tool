import unittest

from ui.shell import (
    APP_SHELL,
    ScreenId,
    SidebarDestinationId,
    ZoneRole,
    get_screen_descriptor,
    get_screen_descriptors,
    get_sidebar_destinations,
)


class UiShellSkeletonTest(unittest.TestCase):
    def test_sidebar_destinations_are_stable(self) -> None:
        destination_ids = [
            destination.destination_id
            for destination in get_sidebar_destinations()
        ]

        self.assertEqual(
            [
                SidebarDestinationId.HOME,
                SidebarDestinationId.PROFILES,
                SidebarDestinationId.HISTORY,
                SidebarDestinationId.HELP,
                SidebarDestinationId.SETTINGS,
            ],
            destination_ids,
        )

    def test_automations_are_not_sidebar_destinations(self) -> None:
        sidebar_labels = {
            destination.label.lower()
            for destination in get_sidebar_destinations()
        }
        sidebar_ids = {
            destination.destination_id.value
            for destination in get_sidebar_destinations()
        }

        self.assertNotIn("automations", sidebar_labels)
        self.assertNotIn("auto1", sidebar_ids)
        self.assertNotIn("auto2", sidebar_ids)
        self.assertNotIn("auto3", sidebar_ids)

    def test_screen_descriptors_exist(self) -> None:
        screen_ids = {
            screen_descriptor.screen_id
            for screen_descriptor in get_screen_descriptors()
        }

        self.assertEqual(
            {
                ScreenId.HOME,
                ScreenId.AUTOMATION_ENVIRONMENT,
                ScreenId.HISTORY,
                ScreenId.PROFILES,
                ScreenId.HELP,
                ScreenId.SETTINGS,
            },
            screen_ids,
        )

    def test_each_screen_has_one_primary_intention(self) -> None:
        for screen_descriptor in get_screen_descriptors():
            self.assertIsInstance(screen_descriptor.primary_intention, str)
            self.assertTrue(screen_descriptor.primary_intention.strip())
            self.assertNotIn("\n", screen_descriptor.primary_intention)
            self.assertNotIn(";", screen_descriptor.primary_intention)

    def test_weighted_zones_preserve_primary_secondary_tertiary_structure(self) -> None:
        for screen_descriptor in get_screen_descriptors():
            zone_roles = [
                zone.role
                for zone in screen_descriptor.zones.as_tuple()
            ]

            self.assertEqual(
                [
                    ZoneRole.PRIMARY,
                    ZoneRole.SECONDARY,
                    ZoneRole.TERTIARY,
                ],
                zone_roles,
            )

    def test_app_shell_defaults_to_home(self) -> None:
        self.assertEqual(ScreenId.HOME, APP_SHELL.default_screen_id)

    def test_screen_descriptor_lookup(self) -> None:
        history_descriptor = get_screen_descriptor(ScreenId.HISTORY)

        self.assertEqual("Operational History", history_descriptor.title)
        self.assertIn("trust recovery", history_descriptor.primary_intention)


if __name__ == "__main__":
    unittest.main()
