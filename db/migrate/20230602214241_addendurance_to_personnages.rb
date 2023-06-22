class AddenduranceToPersonnages < ActiveRecord::Migration[6.1]
  def change
    add_column :personnages, :endurance, :integer
  end
end
