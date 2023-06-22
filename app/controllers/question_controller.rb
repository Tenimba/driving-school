class QuestionController < ApplicationController
    before_action :find_quete
    before_action :find_etape, only: [:index, :new, :create, :edit, :update, :destroy]
  
    def index
      if current_user.role == 'player'
        @etape = Etape.find(params[:etape_id])
        @questions = Question.where(etape_id: @etape.id)
        render 'player' # Render the player.html.erb view
      else
        @etape = Etape.find(params[:etape_id])
        @questions = Question.where(etape_id: @etape.id)
      end
    end
  
    def new
      @question = Question.new
      @etape = Etape.find(params[:etape_id])
    end
  
    def create
      @etape = Etape.find(params[:etape_id])
      @question = @etape.questions.build(question_params)
  
      if @question.save
        redirect_to quete_etape_question_index_path, notice: "Question ajoutée avec succès."
      else
        render :new
      end
    end
  
    def edit
      @quete = Quete.find(params[:quete_id])
      @question = Question.find(params[:id])
      @etape = Etape.find(params[:etape_id])
    end
  
    def update
      @question = Question.find(params[:id])
      if @question.update(question_params)
        redirect_to quete_etape_question_index_path, notice: "Question mise à jour avec succès."
      else
        render :edit
      end
    end
  
    def destroy
      @question = Question.find(params[:format])
      @question.destroy
      redirect_to quete_etape_question_index_path, notice: "Question supprimée avec succès."
    end
  
    def valider_questions_quete_etape
        # Récupérer les réponses sélectionnées par l'utilisateur
        selected_reponses = params[:reponses]
        # Vérifier les réponses et mettre à jour la vie de l'utilisateur en conséquence
        @user = current_user
        if @user.role == 'player'
          # Vérifier si les réponses sélectionnées sont correctes
          @etape = Etape.find(params[:id])
          @questions = Question.where(etape_id: @etape.id).first(3)
      
          # Calculer le nombre de réponses incorrectes
          incorrect_answers_count = 0
      
          @questions.each do |question|
            selected_answer_ids = selected_reponses[question.id.to_s].split(',').map(&:to_i)
            correct_answer_ids = question.reponses.where(correcte: true, question_id: question.id).pluck(:id)
            if selected_answer_ids != correct_answer_ids 
                incorrect_answers_count += 1
            end
          end
      
          if incorrect_answers_count.zero?
            xp_gained = @etape.xp # Récupérer la valeur de xp de l'étape
            xpUser = @user.xp || 0
            @user.update(xp: xpUser + xp_gained) # Ajouter xp_gained à user.xp
            Terminer.create(user_id: @user.id, etape_id: @etape.id) # Créer un nouveau Terminer
            flash[:notice] = "Réponses correctes :-)"
            flash[:alert] = "Vous avez gagné #{xp_gained} points d'expérience ! Continuez comme ça !"
            redirect_to quete_etape_index_path(@quete, @etape, quete_id: @quete.id, etape_id: @etape.id, personnage_id: @user.personnage.id) and flash[:notice] and return
          else
            # vie_actuelle = @user.vie || 0
            vie_actuelle = Personnage.find(params[:personnage_id]).vie || 0
            Personnage.find(params[:personnage_id]).update(vie: vie_actuelle - incorrect_answers_count)
            flash[:notice] = "Réponses incorrectes :-#{incorrect_answers_count}"
            flash[:alert] = "Vous avez perdu #{incorrect_answers_count} vies. Pas de panique, vous pouvez retenter votre chance !"
            redirect_to quete_etape_index_path(@quete, @etape, quete_id: @quete.id, etape_id: @etape.id, personnage_id: params[:personnage_id]) and flash[:notice] and return
          end
          
        end
        redirect_to quete_etape_question_index_path(@quete, @etape, quete_id: @quete.id, etape_id: @etape.id, personnage_id: @user.personnage.id) and flash[:notice] and return
      end
      
      
  
    private
  
    def find_quete
      @quete = Quete.find(params[:quete_id])
    end
  
    def find_etape
      @etape = Etape.find(params[:etape_id])
    end
  
    def question_params
      params.require(:question).permit(:content, reponses_attributes: [:id, :contenu, :correcte, :_destroy])
    end

  end
  