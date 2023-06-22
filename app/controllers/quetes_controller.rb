class QuetesController < ApplicationController
  def index
    if current_user && current_user.role == 'game_master'
      # Si l'utilisateur est un game_master, affichez toutes les quêtes liées à ce game_master
      @quetes = current_user.quetes
      puts @quetes
    elsif current_user && current_user.role == 'joueur'
      # Si l'utilisateur est un joueur, récupérez le game_master auquel il est associé via la table intermédiaire
      game_master = current_user.player_game_masters.first.game_master
      # Récupérez les quêtes du game_master
      @quetes = game_master.quetes
      @termine = game_master.quetes.includes(:terminer).where(terminers: {user_id: current_user.id})
    else
      # Si l'utilisateur n'est ni un joueur ni un game_master, affichez toutes les quêtes
      @quetes = Quete.all
    end
  end
  
  def show
    @quete = Quete.find(params[:id])
    @etapes = @quete.etapes
  end

  def new
    @quete = Quete.new
  end

  def create
    @quete = current_user.quetes.build(quete_params)
    # @quete = Quete.new(quete_params)

    if @quete.save
      redirect_to new_quete_element_path(@quete), notice: "Quête créée avec succès. Ajoutez l'element qui sera remporter à la fin de la quête."
      # redirect_to quetes_path, notice: 'Quête créée avec succès.'
    else
      render :new
    end
  end

  def edit
    @quete = Quete.find(params[:id])
  end
  
  def update
    @quete = Quete.find(params[:id])
    if @quete.update(quete_params)
      redirect_to quete_path, notice: "Quête mise à jour avec succès."
    else
      render :edit
    end
  end
  
  def destroy
    @quete = Quete.find(params[:id])
    @quete.destroy
    redirect_to quetes_path, notice: "Quête supprimée avec succès."
  end
  
  private

  def quete_params
    params.require(:quete).permit(:titre, :description)
  end
end
