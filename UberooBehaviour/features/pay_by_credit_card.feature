# Created by nikita at 10/11/2018
Feature: Pay by credit card
  As Erin,
  I can pay directly by credit card on the platform,
  so that I only have to retrieve my food when delivered.

  @skip
  Scenario: Pay by credit card
    Given a customer "Erin" with an order id "42"
     When paying with my credit card number "4050841376945000", CVV "874" and expiracy "09/2025"
     Then the order is marked as paid