# app/models/terminer.rb
class Terminer < ApplicationRecord
    belongs_to :user
    belongs_to :quete
    belongs_to :etape
  end
  