class CreateElements < ActiveRecord::Migration[6.1]
  def change
    create_table :elements do |t|
      t.references :quete, null: false, foreign_key: true
      t.string :image
      t.integer :force
      t.integer :vie
      t.integer :xpplus
      t.integer :element_type

      t.timestamps
    end
  end
end
