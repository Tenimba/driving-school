class AddTypeToEtapes < ActiveRecord::Migration[6.1]
  def change
    add_column :etapes, :type, :string
  end
end
