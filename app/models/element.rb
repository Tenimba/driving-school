class Element < ApplicationRecord
  has_one_attached :image
  belongs_to :quete
  has_and_belongs_to_many :users, join_table: 'elements_users'
  enum element_type: {
    chapeau: 1,
    armes: 2,
    bouclier: 3
  }
  def element_type_label
    case element_type.to_sym
    when :chapeau
      "Chapeau"
    when :armes
      "Armes"
    when :bouclier
      "Bouclier"
    else
      "Type d'élément inconnu"
    end
  end
end
