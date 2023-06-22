class AddGameMasterIdToQuetes < ActiveRecord::Migration[6.1]
  def change
    add_column :quetes, :game_master_id, :integer
  end
end
