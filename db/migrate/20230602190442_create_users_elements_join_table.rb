class CreateUsersElementsJoinTable < ActiveRecord::Migration[6.0]
  def change
    create_table :users_elements, id: false do |t|
      t.belongs_to :user
      t.belongs_to :element
    end
  end
end
