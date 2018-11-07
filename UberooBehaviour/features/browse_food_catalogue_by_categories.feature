# Created by nikita at 07/11/2018
Feature: Browse the food catalogue by categories
  As Gail,
  I can browse the food catalogue by categories,
  so that I can immediately identify my favorite junk food.

  Scenario: Search for sushis saumon meal
    Given a list of food categories
     When listing meals by "Japonais" category
     Then "Sushis saumon" is available at a restaurant
