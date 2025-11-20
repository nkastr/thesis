# locust file for stressing google's eshop application

import random
from locust import HttpUser, TaskSet, between


def login(l):
    username = ""
    password = ""
    l.client.post("/", {'username': username, 'password': password})

def index(l):
    l.client.get("/")

def searchSensors(l):
    l.client.post("/",{})

def subToSensor(l):
    l.client.post()

def searchApps(l):
    l.client.get("/cart")

def searchSubs(l):
    l.client.get("/", {})

def sendDataToSensor(l):
    l.client.post("/", {})

def subToApp(l):
    l.client.post("", {})

def deployMashupApp(l):
    l.client.post("", {})

def accessMashupApp(l):
    l.client.get("", {})

class UserBehavior(TaskSet):

    def on_start(self):
        index(self)

    tasks = {
        login: 1,
        index: 17,
        searchSensors: 11,
        subToSensor: 10,
        searchApps: 12,
        searchSubs: 11,
        sendDataToSensor: 11,
        subToApp: 5,
        deployMashupApp: 1,
        accessMashupApp: 10}

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 10)