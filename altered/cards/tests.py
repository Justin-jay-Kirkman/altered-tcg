import os

from django.test import TestCase
from cards.sim_youtube_videos import get_simulated_videos_by_channel


# Create your tests here.
class SimulateYouTubeVideosTest(TestCase):

    def test_sim_youtube_videos_not_found(self):
        result = get_simulated_videos_by_channel("bob")
        self.assertEqual(result, None)

    def test_sim_youtube_videos_found(self):
        result = get_simulated_videos_by_channel("UC6qq5ZRn_epjgdKwtgmeSd3")
        self.assertGreaterEqual(len(result), 1)
