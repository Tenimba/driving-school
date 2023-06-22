class CreateEtables < ActiveRecord::Migration[6.1]
  def change
    create_table :etables do |t|
      t.references :quete, null: false, foreign_key: true
      t.string :image
      t.integer :force
      t.integer :vie
      t.integer :xpplus
      t.string :type

      t.timestamps
    end
  end
end
