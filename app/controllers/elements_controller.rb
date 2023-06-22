# app/controllers/elements_controller.rb
class ElementsController < ApplicationController

  def index
    if current_user.role == 'game_master'
    @elements = Element.all
    else
    @elements = current_user.elements
    end
  end
  
    def edit
      @element = Element.find(params[:id])
    end
  
    def update
      @element = Element.find(params[:id])
  
      if @element.update(element_params)
        redirect_to elements_path, notice: "Élément mis à jour avec succès."
      else
        render :edit
      end
    end
  
    def destroy
      @element = Element.find(params[:id])
      @element.destroy
  
      redirect_to elements_path, notice: "Élément supprimé avec succès."
    end  

    def new
      @element = @quete.elements.build
    end
  
    def create
      @element = @quete.elements.build(element_params)
    
      if @element.save
        @element.image.attach(params[:element][:image]) if params[:element][:image].present?
        redirect_to quetes_path, notice: "Element créé avec succès."
      else
        render :new
      end
    end  
    private
  
    def set_quete
      @quete = Quete.find(params[:quete_id])
    end
  
    def element_params
      params.require(:element).permit(:image, :force, :vie, :xpplus, :element_type)
    end
  end
  