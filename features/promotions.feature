Feature: The promotion service back-end
    As a Promotion Owner
    I need a RESTful catalog service
    So that I can keep track of all my promotions

Background:
    Given the following promotions
        | ID | Name | Value | Code | Description | Type | Active | Scope | Start Date | End Date | Created By | Modified By | Created When | Modified When |
        | 1 | Promotion A | 10 | CODE1 | Description 1 | ABSOLUTE | True | ENTIRE_STORE | 2024-01-01 | 2024-12-31 | 00000000-0000-0000-0000-000000000000 | 00000000-0000-0000-0000-000000000000 | 2024-01-01 | 2024-01-02 |
        | 2 | Promotion B | 20 | CODE2 | Description 2 | PERCENTAGE | False | PRODUCT_ID | 2024-02-01 | 2024-11-30 | 00000000-0000-0000-0000-000000000000 | 00000000-0000-0000-0000-000000000000 | 2024-02-01 | 2024-02-02 |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Promotion Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Retrieving a promotion
    When I visit the "Home Page"
    And I look for test promotion id "1"
    And I click the "retrieve-btn" button
    Then I should see the promotion details in the form
    | ID | Name | Value | Code | Description | Type | Active | Scope | Start Date | End Date | Created By | Modified By | Created When | Modified When |
    | 1 | Promotion A | 10 | CODE1 | Description 1 | ABSOLUTE | True | ENTIRE_STORE | 2024-01-01 | 2024-12-31 | 00000000-0000-0000-0000-000000000000 | 00000000-0000-0000-0000-000000000000 | 2024-01-01 | 2024-01-02 |