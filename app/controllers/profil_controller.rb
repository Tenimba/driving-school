class ProfilController < ApplicationController
  def show
    @utilisateur = current_user
    @joueur = User.find_by(id: @utilisateur.id)
    @elements = @joueur.elements
    if @joueur.role == 'game_master'
      @players = PlayerGameMaster.where(game_master_id: @joueur.id)
    else
      @vie = @joueur.vie
      @force = @joueur.force
      @xp = @joueur.xp
      @quete = @joueur.quetes
    end
    puts @elements
  end
end
