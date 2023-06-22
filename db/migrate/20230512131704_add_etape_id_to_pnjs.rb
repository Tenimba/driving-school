class AddEtapeIdToPnjs < ActiveRecord::Migration[6.1]
  def change
    add_reference :pnjs, :etape, foreign_key: true
  end
end
