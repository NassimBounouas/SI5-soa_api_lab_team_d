# Created by nikita at 10/11/2018
Feature: Track coursier
  As a customer (Gail, Erin),
  I want to track the geolocation of the coursier in real time,
  so that I can anticipate when I will eat.

  Scenario: Track a coursier while delivering
    Given a client "Erin" with a picked up order id "42"
     When the customer asks from the geolocation of the coursier
     Then the geolocation is returned