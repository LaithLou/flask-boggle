from http.client import responses
from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')

            # test that you're getting a template
            html = response.get_data(as_text=True)
            self.assertIn('<button class="word-input-btn">Go</button>', html)
            self.assertIn("boggle home page", html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post("/api/new-game")
            json_response = response.get_json()

            # write a test for this route
            self.assertIs(type(json_response["gameId"]), str)
            self.assertIs(type(json_response["board"][0]), list)
            self.assertIs(type(json_response["board"]), list)
            self.assertIs(type(json_response["board"]), list)

    def test_api_score_word(self):

        with self.client as client:
            game_id = client.post('/api/new-game').get_json()['gameId']
           # board = client.post('/api/new-game').get_json()['board']
            game = games[game_id]

            for lst in game.board:
                for i in range(len(lst)):
                    lst[i] = 'X'

            game.board[0][0] = "C"
            game.board[0][1] = "A"
            game.board[0][2] = "T"

            response = client.post(
                "/api/score-word", json={'game_id': game_id, 'word': 'STT'})
            json_response = response.get_json()
            self.assertEqual({"result": 'not-word'}, json_response)

            response = client.post(
                "/api/score-word", json={'game_id': game_id, 'word': 'CAT'})
            json_response = response.get_json()
            self.assertEqual({"result": "ok"}, json_response)

            response = client.post(
                "/api/score-word", json={'game_id': game_id, 'word': 'DOG'})
            json_response = response.get_json()
            self.assertEqual({"result": "not_on_board"}, json_response)
