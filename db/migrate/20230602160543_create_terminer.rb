class CreateTerminer < ActiveRecord::Migration[6.1]
  def change
    create_table :terminers do |t|
      t.references :user, null: false, foreign_key: true
      t.references :quete, null: false, foreign_key: true
      t.references :etape, null: false, foreign_key: true

      t.timestamps
    end
  end
end
