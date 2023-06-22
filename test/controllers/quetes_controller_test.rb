require "test_helper"

class QuetesControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get quetes_index_url
    assert_response :success
  end
end
