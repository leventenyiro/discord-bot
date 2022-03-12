import unittest
from utility.mockups import *
from extensions.basic import Basic

class TestPing(unittest.TestCase):
    def test_ping_response(self):
        bot = MockBot()
        cog = Basic(bot)
        ctx = MockContext()
        result = asyncio.run(cog.ping(cog, ctx))
        expected = f'Pong! {round(bot.latency*1000)} ms'
        self.assertEqual(expected,result)
