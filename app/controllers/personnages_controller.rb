class PersonnagesController < ApplicationController

    def index
        @personnages = Personnage.all
    end

    def new
      @personnage = Personnage.new
    end

    def lancer_de
        caracteristique = params[:caracteristique]
        valeur = params[:valeur].to_i
        @personnage = current_user

        @personnage.update(caracteristique => valeur + rand(1.8))
      
        render json: { result: @personnage.send(caracteristique) }
      end

      def select_personnage
        redirect_to quetes_path(personnage_id: params[:personnage_id])
      end

    def create
      @personnage = Personnage.new(personnage_params)
      @personnage.niveau = 1
      if @personnage.save
        redirect_to personnages_path, notice: 'Personnage créé avec succès.'
      else
        render :new
      end
    end

    def edit
      @personnage = Personnage.find(params[:id])
    end
  
    def update
      @personnage = Personnage.find(params[:id])
      if @personnage.update(personnage_params)
        redirect_to @personnage, notice: 'Personnage mis à jour avec succès.'
      else
        render :edit
      end
    end
  
    def destroy
      @personnage = Personnage.find(params[:id])
      @personnage.destroy
      redirect_to personnages_path, notice: 'Personnage supprimé avec succès.'
    end

    def show
      @personnage = Personnage.find(params[:id])
    end

    private
  
    def personnage_params
      params.require(:personnage).permit(:nom, :force, :vie, :xp, :agilite, :charisme, :intelligence, :endurance, :chance)
    end
  end
  