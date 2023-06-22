# app/models/question.rb
class Question < ApplicationRecord
    belongs_to :etape
    has_many :reponses, dependent: :destroy
    accepts_nested_attributes_for :reponses, reject_if: :all_blank, allow_destroy: true
  
    validates :reponses, presence: true
  end
  