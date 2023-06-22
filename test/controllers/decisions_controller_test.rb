require "test_helper"

class DecisionsControllerTest < ActionDispatch::IntegrationTest
  test "should get new" do
    get decisions_new_url
    assert_response :success
  end
end
