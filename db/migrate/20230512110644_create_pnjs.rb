class CreatePnjs < ActiveRecord::Migration[6.1]
  def change
    create_table :pnjs do |t|
      t.integer :vie
      t.integer :force
      t.string :avatar

      t.timestamps
    end
  end
end
