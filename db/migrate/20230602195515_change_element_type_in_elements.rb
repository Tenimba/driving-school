class ChangeElementTypeInElements < ActiveRecord::Migration[6.1]
  def up
    change_column :elements, :element_type, :integer
    rename_column :element_type, :type, :elements
  end

  def down
    change_column :elements, :element_type, :string
  end
end
