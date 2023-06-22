require "application_system_test_case"

class DummiesTest < ApplicationSystemTestCase
  setup do
    @dummy = dummies(:one)
  end

  test "visiting the index" do
    visit dummies_url
    assert_selector "h1", text: "Dummies"
  end

  test "creating a Dummy" do
    visit dummies_url
    click_on "New Dummy"

    click_on "Create Dummy"

    assert_text "Dummy was successfully created"
    click_on "Back"
  end

  test "updating a Dummy" do
    visit dummies_url
    click_on "Edit", match: :first

    click_on "Update Dummy"

    assert_text "Dummy was successfully updated"
    click_on "Back"
  end

  test "destroying a Dummy" do
    visit dummies_url
    page.accept_confirm do
      click_on "Destroy", match: :first
    end

    assert_text "Dummy was successfully destroyed"
  end
end
