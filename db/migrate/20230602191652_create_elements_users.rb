class CreateElementsUsers < ActiveRecord::Migration[6.1]
  def change
    create_table :elements_users do |t|
      t.references :user, null: false, foreign_key: true
      t.references :element, null: false, foreign_key: true
      t.timestamps
    end
  end
end
