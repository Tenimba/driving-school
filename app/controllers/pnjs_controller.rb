class PnjsController < ApplicationController
    before_action :set_etape, only: [:index, :new, :create]
    before_action :set_quete, only: [:index, :new, :create]
    
    def index
        @quete = Quete.find(params[:quete_id])
        @etape = Etape.find(params[:id])
        @user = current_user
        @personnage = Personnage.find(params[:personnage_id])
      
        # Vérifiez si l'utilisateur a le rôle de 'player'
        if @user.role == 'player'
          @pnj = Pnj.where(quete_id: @quete.id, etape_id: @etape.id).where.not(vie: 0).first
          # Affichez la vue du combat
          render 'combat'
        else
          @pnjs = Pnj.where(quete_id: @quete.id, etape_id: @etape.id)
        end
      end

      def attaquer
        @pnj = Pnj.find(params[:pnj_id])
        @quete = Quete.find(params[:quete_id])
        @etape = Etape.find(params[:id])
        @personnage = Personnage.find(params[:personnage_id])
        @persovie = @personnage.attributes['vie']
        @user = current_user
      
        if @user.present? && @personnage.attributes['vie'].positive?
          # Tour du joueur humain
          pnj_vie = @pnj.vie.to_i - @personnage.attributes['force'].to_i
          pnj_vie = 0 if pnj_vie.negative?
          @pnj.update(vie: pnj_vie)
        end
      
        if @pnj.vie.positive? && @personnage.attributes['vie'].positive?
          # Tour du joueur PNJ
          user_vie = @personnage.attributes['vie'].to_i - @pnj.force.to_i
          user_vie = 0 if user_vie.negative?
          @personnage.update_columns(vie: user_vie)
          # @user.update_columns(vie: user_vie)
        end

        if @pnj.vie.zero?
            # Le pnj a perdu
            flash[:notice] = 'Vous avez gagné le combat !'
            xp_gained = @etape.xp # Récupérer la valeur de xp de l'étape
            @user.update(xp: @user.xp + xp_gained) # Ajouter xp_gained à user.xp
            @etape.update(termine: true) # Définir @etape.termine sur true
            redirect_to quete_etape_index_path( @quete.id, @etape.id)
        elsif @personnage.attributes['vie'].zero?
            # Le joueur a perdu
            flash[:notice] = 'Vous avez perdu le combat !'
            xp_gained = @etape.xp # Récupérer la valeur de xp de l'étape
            @user.update(xp: @user.xp - xp_gained) # Retirer les points d'expérience
            @etape.update(termine: true) # Définir @etape.termine sur true
            @personnage.update(vie: 55) # Remettre la vie à 100
            redirect_to quete_etape_index_path( @quete.id, @etape.id)
          else
            # La partie continue, redirection vers la page de combat
            redirect_to quete_pnjs_path(@quete, @etape, personnage_id: params[:personnage_id])
          end          

    end
      
    def new
        @pnj = Pnj.new
        @quete = Quete.find(params[:quete_id])
        @etape = Etape.find(params[:id])
        @pnjs = @etape.pnjs
      end    

    def create
        @pnj = Pnj.new(pnj_params)
        @pnj.etape_id = @etape.id
        @pnj.quete_id = @quete.id
        if @pnj.save
            redirect_to quete_etape_index_path(etape_id: @pnj.etape_id), notice: 'PNJ créé avec succès.'
        else
          flash.now[:alert] = "Erreur lors de la création du PNJ : " + @pnj.errors.full_messages.join(", ")
          render :new
        end
      end
      
      
  
    private
    def pnj_params
        params.require(:pnj).permit(:nom, :vie, :force, :avatar, :etape_id)
      end 
      
    def set_etape
        @etape = Etape.find(params[:id])
    end

    def set_quete
        @quete = Quete.find(params[:quete_id])
    end
  end
  