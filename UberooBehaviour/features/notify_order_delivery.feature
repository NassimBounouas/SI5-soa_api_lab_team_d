# Created by nikita at 10/11/2018
Feature: Notify order delivery
  As Jamie,
  I want to notify that the order has been delivered,
  so that my account can be credited and the restaurant can be informed.

  @skip
  Scenario: Notify that the order has been delivered
    Given a steed "Jamie" with a delivered order id "42"
     When sending notification message of a successful delivery
     Then an order is marked as delivered