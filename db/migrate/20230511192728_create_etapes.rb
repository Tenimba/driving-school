class CreateEtapes < ActiveRecord::Migration[6.1]
  def change
    create_table :etapes do |t|
      t.string :titre
      t.text :description
      t.references :quete, null: false, foreign_key: true

      t.timestamps
    end
  end
end
