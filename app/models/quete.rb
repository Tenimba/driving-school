# app/models/quete.rb
class Quete < ApplicationRecord
    has_many :etapes, dependent: :destroy
    has_many :elements, dependent: :destroy
    has_many :terminer
    belongs_to :game_master, class_name: "User"
  end
  