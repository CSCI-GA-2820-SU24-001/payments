Feature: The promotion service back-end
    As a Promotion Owner
    I need a RESTful catalog service
    So that I can keep track of all my promotions

Background:
    Given the following promotions
        | ID | Name | Value | Code | Description | Type | Active | Scope | Start Date | End Date | Created By | Modified By | Created When | Modified When |
        | 1 | Promotion A | 10 | CODE1 | Description 1 | Type 1 | True | Scope 1 | 2024-01-01 | 2024-12-31 | User 1 | User 2 | 2024-01-01 | 2024-01-02 |
        | 2 | Promotion B | 20 | CODE2 | Description 2 | Type 2 | False | Scope 2 | 2024-02-01 | 2024-11-30 | User 3 | User 4 | 2024-02-01 | 2024-02-02 |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Promotion Demo RESTful Service" in the title
    And I should not see "404 Not Found"