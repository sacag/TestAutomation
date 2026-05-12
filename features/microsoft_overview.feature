Feature: Microsoft Overview Page
  As a visitor to the Microsoft information site
  I want to view the Overview page
  So that I can find accurate information about Microsoft

  Background:
    Given I am on the Microsoft Overview page

  Scenario: Page loads with the correct title
    Then the page title should be "Microsoft - About the Company"

  Scenario: Page displays the main heading
    Then I should see the heading "About Microsoft"

  Scenario: Section "Company Facts" is present
    Then I should see the heading "Company Facts"

  Scenario: Section "Key Products and Services" is present
    Then I should see the heading "Key Products and Services"

  Scenario: Section "Leadership and Culture" is present
    Then I should see the heading "Leadership and Culture"

  Scenario: Section "Artificial Intelligence" is present
    Then I should see the heading "Artificial Intelligence"

  Scenario: Section "Financial Highlights" is present
    Then I should see the heading "Financial Highlights"

  Scenario: Section "Official Resources" is present
    Then I should see the heading "Official Resources"

  Scenario: Section "Learn More" is present
    Then I should see the heading "Learn More"

  Scenario: Page contains expected body text
    Then the page body should contain "Microsoft Corporation is an American multinational technolog"

  Scenario: Page contains expected body text
    Then the page body should contain "Headquarters: Redmond, Washington, USA"

  Scenario: External links are present on the page
    Then the link "Microsoft Investor Relations" should be present
    And the link "Microsoft Official Website" should be present
    And the link "Microsoft Azure" should be present
    And the link "Microsoft on GitHub" should be present
    And the link "Microsoft on LinkedIn" should be present
    And the link "Microsoft on Wikipedia" should be present
    And the link "Microsoft Blog" should be present

  Scenario: External links open a reachable page in a new browser tab
    Then the link "Microsoft Investor Relations" should open a reachable page in a new tab
    And the link "Microsoft Official Website" should open a reachable page in a new tab
    And the link "Microsoft Azure" should open a reachable page in a new tab
    And the link "Microsoft on GitHub" should open a reachable page in a new tab
    And the link "Microsoft on LinkedIn" should open a reachable page in a new tab
    And the link "Microsoft on Wikipedia" should open a reachable page in a new tab
    And the link "Microsoft Blog" should open a reachable page in a new tab

  Scenario: Navigation link is present and functional
    When I click the link "Microsoft History"
    Then I should be on the History page
