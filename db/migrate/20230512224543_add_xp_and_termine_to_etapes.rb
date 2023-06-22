class AddXpAndTermineToEtapes < ActiveRecord::Migration[6.1]
  def change
    add_column :etapes, :xp, :integer
    add_column :etapes, :termine, :boolean
  end
end
