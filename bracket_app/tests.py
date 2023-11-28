from django.test import TestCase, Client, LiveServerTestCase
from .models import *
from .generator import Generator
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import time

class TestModels(TestCase):
    def setUp(self):
        self.tournament = Tournament.objects.create(
            creator="john",
            title="bracket1",
            players="ram\ngarfiel\nreinhard\nemilia\nsubaru",
            completed=False,
        )

    def test(self):
        url = reverse("tournament-detail", kwargs={"pk": self.tournament.pk})

        self.assertEqual(self.tournament.creator, "john")
        self.assertEqual(self.tournament.title, "bracket1")
        self.assertEqual(self.tournament.players, "ram\ngarfiel\nreinhard\nemilia\nsubaru")
        self.assertEqual(self.tournament.completed, False)
        self.assertEqual(self.tournament.get_absolute_url(), url)
        self.assertEqual(str(self.tournament), "bracket1")


class TestViews(TestCase):
    def setUp(self):
        self.tournament = Tournament.objects.create(
            creator="mike",
            title="bracket2",
            players = json.dumps(["elsa", "frederica", "julius", "betelgeuse", "satella"]),
            completed=False,
        )

    def test_tournament_detail_view(self):
        url = reverse('tournament-detail', args=[self.tournament.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bracket_app/tournament_detail.html')
        self.assertEqual(response.context['tournament'], self.tournament)
        self.assertEqual(response.context['player_list'], ["elsa", "frederica", "julius", "betelgeuse", "satella"])
        self.assertEqual(response.context['path'], f"bracket_images/{self.tournament.pk}_bracket.png")
        self.assertEqual(response.context['size'], 5)
    

class TestGenerator(TestCase):
    def setUp(self):
        self.generator = Generator(
            800,
            700,
            50,
            ["roswaal", "echidna", "beatrice", "rem", "pandora"],
            123,
            is_testing=True
        )

    def test(self):
        self.assertEqual(self.generator.is_testing, True)
        self.assertEqual(self.generator.width, 800)
        self.assertEqual(self.generator.height, 700)   
        self.assertEqual(self.generator.padding, 50)    
        self.assertEqual(self.generator.player_list, ["roswaal", "echidna", "beatrice", "rem", "pandora"])
        self.assertEqual(self.generator.list_size, 5)
        self.assertEqual(self.generator.num_columns, 4)
        self.assertEqual(self.generator.entry_width, 175)
        self.assertEqual(self.generator.entry_height, 160)
        self.assertEqual(self.generator.font_size, 29)
        self.assertEqual(self.generator.pk, 123)

        self.generator.draw()
        self.assertEqual(self.generator.path, "bracket_app/static/bracket_images/123_bracket.png")


class TestNavbar(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_navbar(self):
        self.browser.get("http://127.0.0.1:8000/")
        self.browser.set_window_size(1920, 1080)

        home_link = By.LINK_TEXT, "Home"
        tournaments_link = By.LINK_TEXT, "Tournaments"
        create_link = By.LINK_TEXT, "Create"
        login_link = By.LINK_TEXT, "Login"

        self.browser.find_element(*home_link).click()
        self.browser.find_element(*tournaments_link).click()
        self.browser.find_element(*create_link).click()
        self.browser.find_element(*login_link).click()

class TestLogin(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_login(self):
        self.browser.get("http://127.0.0.1:8000/")
        self.browser.set_window_size(1920, 1080)
        login_link = By.LINK_TEXT, "Login"
        self.browser.find_element(*login_link).click()

        username_input = self.browser.find_element(By.ID, 'id_username')
        username_input.send_keys('TestUser')

        password_input = self.browser.find_element(By.ID, 'id_password')
        password_input.send_keys('test12345')

        login = self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="login"]')
        login.click()

