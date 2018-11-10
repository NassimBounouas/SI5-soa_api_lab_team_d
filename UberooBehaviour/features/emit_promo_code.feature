# Created by nikita at 10/11/2018
Feature: Emit a promotional code
  As Terry,
  I can emit a promotional code,
  so that I can attract more customer to my restaurant.

  Scenario: Emit a promo code
    Given a restaurant "Dragon d'Or"
     When creating a new promo code "5OFF" giving a "5%" discount
     Then customers can use this promo code for reducing the cost of an order