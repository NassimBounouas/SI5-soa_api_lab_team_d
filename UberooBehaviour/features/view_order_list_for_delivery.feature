# Created by nikita at 10/11/2018
Feature: View order list for delivery
  As Jamie,
  I want to know the orders that will have to be delivered around me,
  so that I can choose one and go to the restaurant to begin the course.

  @skip
  Scenario: View orders around position
    Given a steed "Jamie" with a GPS position "43.700000,7.250000"
     When listing available orders around
     Then an order collection is fetched