import unittest
from unittest.mock import MagicMock, patch

from abcvaultbot.config import DiscordConfig, NotificationConfig
from abcvaultbot.notifications import Notifier


class DiscordNotificationTests(unittest.TestCase):
    @patch("abcvaultbot.notifications.requests.post")
    def test_discord_sends_content(self, mock_post: MagicMock) -> None:
        mock_post.return_value.status_code = 204
        config = NotificationConfig(
            console=False,
            discord=DiscordConfig(
                enabled=True,
                webhook_url="https://discord.com/api/webhooks/test/token",
            ),
        )
        Notifier(config).send("Added to cart", "Blanton's\nhttps://theabcvault.com/cart.php")
        mock_post.assert_called_once()
        payload = mock_post.call_args.kwargs["json"]
        self.assertIn("Added to cart", payload["content"])
        self.assertIn("Blanton", payload["content"])


if __name__ == "__main__":
    unittest.main()
