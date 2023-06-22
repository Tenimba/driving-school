class CreateQuetes < ActiveRecord::Migration[6.1]
  def change
    create_table :quetes do |t|
      t.string :titre
      t.text :description

      t.timestamps
    end
  end
end
