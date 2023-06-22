class User < ApplicationRecord
  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable, :trackable and :omniauthable
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :validatable
  
  has_many :quetes, foreign_key: :game_master_id, dependent: :destroy
  has_many :player_game_masters, foreign_key: :player_id
  has_many :game_masters, through: :player_game_masters
  has_many :terminer
  has_and_belongs_to_many :elements, join_table: 'elements_users'
  attr_accessor :vie, :force

  after_create :assign_default_values

  private

  def assign_default_values
    if game_master?
      # Ne rien faire, les game masters gardent les valeurs par défaut (null)
    else
      # Les players ont des valeurs par défaut
      update(vie: 5, force: 10)
    end
  end

  def game_master?
    role == 'game_master'
  end
end