class RenameTypeToElementTypeInElements < ActiveRecord::Migration[6.1]
  def change
    rename_column :elements, :type, :element_type
  end
end
