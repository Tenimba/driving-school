class AddReferenceToPnjs < ActiveRecord::Migration[6.1]
  def change
    add_reference :pnjs, :quete, foreign_key: true
  end
end
