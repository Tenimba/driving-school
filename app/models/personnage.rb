
class Personnage < ApplicationRecord
    validates :nom, presence: true
  
    def lancer_de_force
      Dice.roll('1d6').result
    end
  
    def lancer_de_vie
      Dice.roll('1d20').result
    end
  
    def lancer_de_xp
      Dice.roll('1d10').result
    end
  
    def lancer_de_agilite
      Dice.roll('1d12').result
    end
  
    def lancer_de_charisme
      Dice.roll('1d10').result
    end
  
    def lancer_de_intelligence
      Dice.roll('1d12').result
    end
  
    def lancer_de_endurance
      Dice.roll('1d8').result
    end
  
    def lancer_de_chance
      Dice.roll('1d20').result
    end

    def increase_xp(amount)
        self.xp += amount
        save
      end
  end
  