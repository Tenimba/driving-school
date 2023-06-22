class AddNomToPnjs < ActiveRecord::Migration[6.1]
  def change
    add_column :pnjs, :nom, :string
  end
end
