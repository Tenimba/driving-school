class AddAttributesToUsers < ActiveRecord::Migration[6.1]
  def change
    add_column :users, :vie, :integer
    add_column :users, :force, :integer
  end
end
