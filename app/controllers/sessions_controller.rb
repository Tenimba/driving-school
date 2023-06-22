class SessionsController < Devise::SessionsController
    private
  
    def after_sign_in_path_for(resource)
      # Redirigez l'utilisateur vers l'endroit souhaité après sa connexion réussie
      if current_user.role == 'game_master'
        quetes_path
      else
        personnages_path
      end
    end
  end
  