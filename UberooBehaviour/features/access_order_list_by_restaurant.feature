# Created by nikita at 07/11/2018
Feature: Access the order list by restaurant
  As Jordan,
  I want to access to the order list,
  so that I can prepare the meal efficiently.

  @skip
  Scenario: Read the preparation dupes
    Given a restaurant "Dragon d'Or" with at least two orders
     When listing dupes for my restaurant
     Then an order collection is fetched