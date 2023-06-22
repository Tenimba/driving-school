class ChoixController < ApplicationController
    before_action :set_quete
    before_action :set_etape

        def combat
          # Récupérer les données nécessaires pour le combat (PNJ, caractéristiques, etc.)
          # Effectuer les calculs de combat et mettre à jour les caractéristiques du joueur
      
          # Rediriger vers la page de résultat du combat ou vers l'étape suivante de la quête
        end
      
        def traiter_combat
            # Récupérer les données du formulaire
            combatant = current_user
            # Traiter le combat et mettre à jour les caractéristiques du combattant
          
            # Rediriger vers la page de résultats du combat ou vers l'étape suivante de la quête
          end
          
      
    def choix
      # Afficher la page de choix (questionnaire ou combat)
    end
  
    def traiter_choix
      choix = params[:choix]
      Rails.logger.debug current_user.role 
      if choix == 'questionnaire'
        redirect_to quete_etape_question_index_path(@quete, @etape, personnage_id: params[:personnage_id])
      elsif choix == 'combat'
        if current_user.role == "game_master"
            redirect_to new_quete_pnj_path(@quete, @etape, personnage_id: params[:personnage_id])
        else
            redirect_to quete_pnjs_path(@quete, @etape, personnage_id: params[:personnage_id])
        end
      else
        redirect_to quete_etape_decision_index_path(@quete, @etape, personnage_id: params[:personnage_id]), alert: "Veuillez sélectionner un choix valide."
      end
    end
  
    private
  
    def set_quete
      @quete = Quete.find(params[:quete_id])
    end
  
    def set_etape
      @etape = Etape.find(params[:id])
    end

  end
  