Rails.application.routes.draw do
  resources :dummies
  get 'decisions/new'
  root 'personnages#index' # Définit la route racine

 resources :elements, only: [:new, :create, :index, :update, :destroy, :edit]
 get 'profil', to: 'profil#show'

 resources :personnages, only: [:new, :create, :index, :update, :destroy, :edit, :show]
 post '/personnages/lancer_de', to: 'personnages#lancer_de'
 get '/select_personnage', to: 'personnages#select_personnage', as: 'select_personnage'
 scope '/personnages/:personnage_id' do
  resources :quetes, except: [:show] do
    resources :etape do
      post '/quetes/:quete_id/etape/:id', to: 'etape#new', as: 'create_etape' 
      patch '/quetes/:quete_id/etape/:id', to: 'etape#update', as: 'update_etape'
      member do
        get 'choix', to: 'choix#choix', as: 'choix_etape'
        post 'traiter_choix', to: 'choix#traiter_choix', as: 'traiter_choix_etape'
        post 'valider_questions', to: 'question#valider_questions_quete_etape', as: 'valider_question_quete_etape'
        get 'combat', to: 'choix#combat', as: 'combat_etape'
        post 'traiter_combat', to: 'choix#traiter_combat', as: 'traiter_combat_etape'
        resources :pnjs, only: [:new, :create, :index, :update, :destroy, :edit, :attaquer]
        post 'quetes/:quete_id/etape/:id/pnjs/:pnj_id/attaquer', to: 'pnjs#attaquer', as: 'attaquer_quete_etape_pnj'
        post '/create_pnj_quete_etape', to: 'pnjs#create', as: 'create_pnj_quete_etape'
      end
      resources :question, only: [:new, :create, :index, :update, :destroy, :edit]
      # resources :elements, only: [:new, :create, :index, :update, :destroy, :edit]
    end
  end
  end

  devise_for :users, controllers: {
    registrations: 'registrations',
    sessions: 'sessions'
  }
end
