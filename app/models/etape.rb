# app/models/etape.rb
class Etape < ApplicationRecord
  belongs_to :quete
  has_many :questions
  has_many :pnjs
  
  attribute :xp, :integer
  attribute :termine, :boolean, default: false
end
