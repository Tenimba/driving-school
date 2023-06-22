# app/controllers/etapes_controller.rb
class EtapeController < ApplicationController
    before_action :set_quete
    before_action :set_etape, only: [:show, :edit, :update, :destroy]
    before_action :set_etape, except: [:new, :create, :index]
     
    def nouveau_pnj
      @pnj = Pnj
    end

    def index
      @etapes = @quete.etapes
      puts @etapes
      @termine = Terminer.includes(:quete).where(quete: @quete, user: current_user, etape: @etapes)
    end
  
    def show
    end
  
    def new
      @quete = Quete.find(params[:quete_id])
      @etape = @quete.etapes.build
    end
  
    def create
      @etape = @quete.etapes.build(etape_params)
      if @etape.save
        redirect_to quete_etape_index_path(@quete), notice: "Étape créée avec succès."
      else
        render :new
      end
    end
  
    def edit
    end
  
    def update
      if @etape.update(etape_params)
        redirect_to quete_etape_path(@quete), notice: "Étape mise à jour avec succès."
      else
        render :edit
      end
    end
  
    def destroy
      @etape.destroy
      redirect_to quete_etape_path(@quete), notice: "Étape supprimée avec succès."
    end
  
    private
  
    def set_quete
      @quete = Quete.find(params[:quete_id])
    end
  
    def set_etape
      @etape = @quete.etapes.find(params[:id])
    end
  
    def etape_params
      params.require(:etape).permit(:titre, :description, :xp)
    end
  end
  