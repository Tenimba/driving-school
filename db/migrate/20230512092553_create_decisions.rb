class CreateDecisions < ActiveRecord::Migration[6.1]
  def change
    create_table :decisions do |t|
      t.references :etape, null: false, foreign_key: true
      t.string :action

      t.timestamps
    end
  end
end
