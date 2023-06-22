# app/models/reponse.rb
class Reponse < ApplicationRecord
    belongs_to :question
    self.table_name = 'reponses'
  end
  