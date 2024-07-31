Feature: The promotion service back-end
    As a Promotion Owner
    I need a RESTful catalog service
    So that I can keep track of all my promotions

Background:
    Given the following promotions
        | ID | Name | Value | Code | Description | Type | Active | Scope | Start Date | End Date | Created By | Modified By | Created When | Modified When |
        | 1 | Promotion A | 10 | CODE1 | Description 1 | ABSOLUTE | True | ENTIRE_STORE | 2024-01-01 | 2024-12-31 | 00000000-0000-0000-0000-000000000000 | 00000000-0000-0000-0000-000000000000 | 2024-01-01 | 2024-01-06 |
        | 2 | Promotion B | 20 | CODE2 | Description 2 | PERCENTAGE | False | PRODUCT_ID | 2024-06-01 | 2024-12-31 | 00000000-0000-0000-0000-000000000000 | 00000000-0000-0000-0000-000000000000 | 2024-01-01 | 2025-01-01 |
        | 3 | Promotion C | 30 | CODE3 | Description 3 | PERCENTAGE | False | PRODUCT_ID | 2023-01-01 | 2024-01-01 | 00000000-0000-0000-0000-000000000000 | 00000000-0000-0000-0000-000000000000 | 2023-02-01 | 2023-02-02 |

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
    | 1 | Promotion A | 10 | CODE1 | Description 1 | ABSOLUTE | True | ENTIRE_STORE | 2024-01-01 | 2024-12-31 | 00000000-0000-0000-0000-000000000000 | 00000000-0000-0000-0000-000000000000 | 2024-01-01 | 2024-01-06 |

Scenario: Querying all promotions
    When I visit the "Home Page"
    And I click the "search-btn" button
    Then I should see names "Promotion A, Promotion B, Promotion C" in the search result table

Scenario: Querying promotions with filters
    When I visit the "Home Page"
    And I enter "06020020241000AM" into the "search_promotion_date" field
    And I click the "search-btn" button
    Then I should see names "Promotion A, Promotion B" in the search result table
    Then I should not see names "Promotion C" in the search result table
    When I enter "PRODUCT_ID" into the "search_promotion_scope" field
    And I click the "search-btn" button
    Then I should see names "Promotion B" in the search result table
    Then I should not see names "Promotion A, Promotion C" in the search result table
