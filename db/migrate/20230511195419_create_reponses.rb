class CreateReponses < ActiveRecord::Migration[6.1]
  def change
    create_table :reponses do |t|
      t.text :contenu
      t.boolean :correcte
      t.references :question, null: false, foreign_key: true

      t.timestamps
    end
  end
end
