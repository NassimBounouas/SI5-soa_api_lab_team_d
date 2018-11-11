# Created by nikita at 10/11/2018
Feature: Order from restaurant and deliver to home
  As Gail or Erin,
  I can order my lunch from a restaurant,
  so that the food is delivered to my place.

  Scenario: Order a lunch from a restaurant
    Given a customer "Gail" that wants to eat "Sushis saumon" at "Gail's home"
     When "Gail" is browsing the menu correspoding to the category "Japonais" and he selects "Sushis saumon"
     Then "Gail" is ordering the meal from the right restaurant to be delivered at "Gail's home"
     Then A delivery request is created