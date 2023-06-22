class AddQuestionIdToReponses < ActiveRecord::Migration[6.1]
  def change
    add_reference :reponses, :question, null: false, foreign_key: true
  end
end
