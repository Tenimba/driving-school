class PlayerGameMaster < ApplicationRecord
    belongs_to :player, class_name: 'User'
    belongs_to :game_master, class_name: 'User'
  end
  