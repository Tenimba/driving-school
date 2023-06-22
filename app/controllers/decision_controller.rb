class DecisionController < ApplicationController
  before_action :find_etape, only: [:index, :update]

  def index
    @quete = Quete.find(params[:quete_id])
    @etape = Etape.find(params[:etape_id])
    @decision = Decision.new
  end


  def update
    respond_to do |format|
      if @decision.update(decision_params)
        if @decision.is_questionnaire
          format.html { redirect_to quete_etape_question_index_path(@quete, @etape), notice: 'La décision a été mise à jour avec succès.' }
        else
          format.html { redirect_to new_quete_etape_combat_path(@quete, @etape), notice: 'La décision a été mise à jour avec succès.' }
        end
        format.json { render :show, status: :ok, location: @decision }
      else
        format.html { render :edit }
        format.json { render json: @decision.errors, status: :unprocessable_entity }
      end
    end
  end
  

  private

  def find_etape
    @quete = Quete.find(params[:quete_id])
    @etape = @quete.etapes.find(params[:etape_id])
  end

  def decision_params
    params.require(:decision).permit(:action)
  end
end
