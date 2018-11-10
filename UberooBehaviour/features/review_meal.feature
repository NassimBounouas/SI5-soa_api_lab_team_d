# Created by nikita at 10/11/2018
Feature: Review meals
  As Jordan,
  I want the customers to be able to review the meals,
  so that I can improve them according to their feedback.

  @skip
  Scenario: Review a meal
    Given a customer "Erin" with an order that contains "Sushis saumon"
     When leaving a review on meal "Sushis saumon"
     Then the feedback is readable by the chief