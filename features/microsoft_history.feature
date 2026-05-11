Feature: Microsoft History Page
  As a visitor to the Microsoft information site
  I want to view the History page
  So that I can find accurate information about Microsoft

  Background:
    Given I am on the Microsoft History page

  Scenario: Page loads with the correct title
    Then the page title should be "Microsoft History - Key Milestones"

  Scenario: Page displays the main heading
    Then I should see the heading "Microsoft History"

  Scenario: Section "1975 - The Beginning" is present
    Then I should see the heading "1975 - The Beginning"

  Scenario: Section "1980 - The IBM Deal" is present
    Then I should see the heading "1980 - The IBM Deal"

  Scenario: Section "1985 - Windows 1.0 Launch" is present
    Then I should see the heading "1985 - Windows 1.0 Launch"

  Scenario: Section "1986 - IPO and Wealth Creation" is present
    Then I should see the heading "1986 - IPO and Wealth Creation"

  Scenario: Section "1990 - Microsoft Office" is present
    Then I should see the heading "1990 - Microsoft Office"

  Scenario: Section "1995 - Windows 95 and the Internet Era" is present
    Then I should see the heading "1995 - Windows 95 and the Internet Era"

  Scenario: Section "2001 - Xbox and Windows XP" is present
    Then I should see the heading "2001 - Xbox and Windows XP"

  Scenario: Section "2008 - Failed Yahoo Bid" is present
    Then I should see the heading "2008 - Failed Yahoo Bid"

  Scenario: Section "2011 - Skype Acquisition" is present
    Then I should see the heading "2011 - Skype Acquisition"

  Scenario: Section "2014 - The Nadella Era Begins" is present
    Then I should see the heading "2014 - The Nadella Era Begins"

  Scenario: Section "2016 - LinkedIn Acquisition" is present
    Then I should see the heading "2016 - LinkedIn Acquisition"

  Scenario: Section "2018 - GitHub Acquisition" is present
    Then I should see the heading "2018 - GitHub Acquisition"

  Scenario: Section "2020 - Teams and Remote Work" is present
    Then I should see the heading "2020 - Teams and Remote Work"

  Scenario: Section "2023 - AI Leadership with OpenAI" is present
    Then I should see the heading "2023 - AI Leadership with OpenAI"

  Scenario: Section "Today" is present
    Then I should see the heading "Today"

  Scenario: Page contains expected body text
    Then the page body should contain "Microsoft's journey from a two-person startup to one of the "

  Scenario: Page contains expected body text
    Then the page body should contain "Bill Gates and Paul Allen founded Microsoft on April 4, 1975"

  Scenario: External links open in a new browser tab
    Then the link "Bill Gates" should be present
    And the link "Bill Gates" should open in a new tab
    And the link "Paul Allen" should be present
    And the link "Paul Allen" should open in a new tab
    And the link "Windows 1.0" should be present
    And the link "Windows 1.0" should open in a new tab
    And the link "Windows 95" should be present
    And the link "Windows 95" should open in a new tab
    And the link "Xbox" should be present
    And the link "Xbox" should open in a new tab
    And the link "Satya Nadella" should be present
    And the link "Satya Nadella" should open in a new tab
    And the link "Microsoft Azure" should be present
    And the link "Microsoft Azure" should open in a new tab
    And the link "GitHub" should be present
    And the link "GitHub" should open in a new tab
    And the link "OpenAI" should be present
    And the link "OpenAI" should open in a new tab

  Scenario: Navigation link is present and functional
    When I click the link "Home - About Microsoft"
    Then I should be on the Overview page
