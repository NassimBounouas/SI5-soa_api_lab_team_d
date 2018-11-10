# Created by nikita at 10/11/2018
Feature: Read statistics
  As Terry,
  I want to get some statistics (speed, cost) about global delivery time and delivery per coursier,
  so that I can make my reporting.

  @skip
  Scenario: Get delivery time of a coursier
    Given a steed "Jamie"
     When computing kpi "delivery time"
     Then the kpi is returned

  @skip
  Scenario: Get delivery performance of a coursier
    Given a steed "Jamie"
     When computing kpi "performance"
     Then the kpi is returned