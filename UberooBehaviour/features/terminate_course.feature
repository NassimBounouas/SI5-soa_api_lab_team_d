# Created by nikita at 10/11/2018
Feature: Terminate course
  As Jamie,
  I want to inform quickly that I can't terminate the course (accident, sick),
  so that the order can be replaced.

  @skip
  Scenario: Terminate a course because of an accident
    # this scenario may be inspired by real facts, that happened this week.
    Given an order "42" being delivered by "Jamie"
     When the steed notify that an issue preventing the delivery happened
     Then the order is rescheduled