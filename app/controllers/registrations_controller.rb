class RegistrationsController < Devise::RegistrationsController
    private
  
    def sign_up_params
        print params
      params.require(:user).permit(:name, :email, :password, :password_confirmation, :role)
    end
  
    def after_sign_up_path_for(resource)
      # Redirigez l'utilisateur vers l'endroit souhaité après son inscription réussie
      user_session_path
    end
  end
  