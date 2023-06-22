class AddEtapeRefToQuestions < ActiveRecord::Migration[6.1]
  def change
    add_reference :questions, :etape, null: false, foreign_key: true
  end
end
