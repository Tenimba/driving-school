class CreatePersonnages < ActiveRecord::Migration[6.1]
  def change
    create_table :personnages do |t|
      t.string :nom
      t.integer :niveau
      t.integer :vie
      t.integer :force
      t.integer :agilite
      t.integer :intelligence
      t.integer :charisme
      t.integer :chance

      t.timestamps
    end
  end
end
