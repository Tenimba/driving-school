class RemoveQueteIdFromPnjs < ActiveRecord::Migration[6.1]
  def change
    remove_column :pnjs, :quete_id, :integer
  end
end
