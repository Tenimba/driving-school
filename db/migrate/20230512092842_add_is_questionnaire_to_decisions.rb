class AddIsQuestionnaireToDecisions < ActiveRecord::Migration[6.1]
  def change
    add_column :decisions, :is_questionnaire, :boolean
  end
end
