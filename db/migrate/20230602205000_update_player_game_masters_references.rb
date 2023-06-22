class UpdatePlayerGameMastersReferences < ActiveRecord::Migration[6.1]
  def change
    remove_reference :player_game_masters, :player, index: true
    remove_reference :player_game_masters, :game_master, index: true
  
    add_reference :player_game_masters, :player, foreign_key: { to_table: :users }
    add_reference :player_game_masters, :game_master, foreign_key: { to_table: :users }
  end
  
end
