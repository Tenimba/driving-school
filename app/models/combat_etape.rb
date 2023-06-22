class CombatEtape < Etape
    has_many :pnjs, dependent: :destroy
    accepts_nested_attributes_for :pnjs, reject_if: :all_blank, allow_destroy: true
  end