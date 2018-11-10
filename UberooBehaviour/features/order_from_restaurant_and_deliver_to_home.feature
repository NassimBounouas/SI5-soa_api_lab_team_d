# Created by nikita at 10/11/2018
Feature: Order from restaurant and deliver to home
  As Gail or Erin,
  I can order my lunch from a restaurant,
  so that the food is delivered to my place.

  @skip
  Scenario: Order a lunch from a restaurant
    Given a customer "Gail" that wants to eat "Sushis saumon"
     When the order is marked as ready for pickup
     Then the order is available for pickup by steeds

  @skip
  Scenario: Deliver a lunch to a place
    Given a customer "Gail" and its last order ready for pickup
     When the order is to customer place
     Then the order is marked as delivered