from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.test import Client
from mixer.backend.django import mixer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from products.models import Product
from django.urls import reverse
import selenium.webdriver.support.ui as ui
import time
import pytest

chrome_options = webdriver.ChromeOptions()


# chrome_options.add_argument("--headless")


class ChromeFunctionalTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()  # (options=chrome_options)
        self.driver.maximize_window()
        self.user = get_user_model()
        self.client = Client()

        # self.driver.implicitly_wait(10)
        # self.wait = ui.WebDriverWait(self.driver, 5)

    def tearDown(self):
        self.driver.close()

    def get_element(self, selector):
        return self.driver.find_element_by_css_selector(selector)

    def test_user_can_connect_and_disconnect(self):
        self.user.objects.create_user(
            username="LeonardCOLIN", password="1234Testing!"
        )

        self.driver.get(self.live_server_url)

        # User is on the homepage and clicks on the login button
        self.get_element("#button-login").click()

        time.sleep(1)

        # Assert the current url is the login url
        assert self.driver.current_url == self.live_server_url + reverse('login') + "?next=/"

        self.get_element("#id_username").send_keys("LeonardCOLIN")
        self.get_element("#id_password").send_keys("1234Testing!")
        self.get_element("#button-connexion").click()

        time.sleep(3)

        # Assert the current url is the home url
        assert self.driver.current_url == self.live_server_url + reverse("home")
        # Assert the profile link is available once user is authenticated
        assert "button-profile" in self.driver.page_source

        # User clicks on the logout button
        self.get_element("#button-logout").click()
        time.sleep(1)
        # Assert user is logged out
        assert "Vous êtes bien déconnecté" in self.driver.page_source

    def test_user_can_register(self):
        self.driver.get(self.live_server_url)

        # User is on the homepage and clicks on the register button
        self.get_element("#button-register").click()

        # Assert the current url is the login url
        assert self.driver.current_url == self.live_server_url + reverse('register') + "?next=/"
        time.sleep(2)

        self.get_element("#id_username").send_keys("Leonard")
        self.get_element("#id_email").send_keys("leocolin@leo.com")
        self.get_element("#id_password1").send_keys("testPassword1234")
        self.get_element("#id_password2").send_keys("testPassword1234")
        time.sleep(2)
        self.get_element("#button-validate").click()
        time.sleep(1)
        assert "Bonjour Leonard" in self.driver.page_source
