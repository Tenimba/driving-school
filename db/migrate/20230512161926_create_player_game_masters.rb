class CreatePlayerGameMasters < ActiveRecord::Migration[6.1]
  def change
    create_table :player_game_masters do |t|
      t.integer :player_id
      t.integer :game_master_id

      t.timestamps
    end
  end
end
