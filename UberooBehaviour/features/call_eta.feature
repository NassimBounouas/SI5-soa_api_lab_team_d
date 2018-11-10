# Created by nikita at 10/11/2018
Feature: Call ETA
  As Erin,
  I want to know before ordering the estimated time of delivery of the meal,
  so that I can schedule my work around it and be ready when it arrives.

  Scenario: Estimate time of arrival of an order
    Given a customer "Erin" with an order "42"
     When calling the ETA service for my order
     Then an estimated time of arrival is provided