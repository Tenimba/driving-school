class AddXpToPersonnages < ActiveRecord::Migration[6.1]
  def change
    add_column :personnages, :xp, :integer
  end
end
