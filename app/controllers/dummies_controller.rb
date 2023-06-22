class DummiesController < ApplicationController
  before_action :set_dummy, only: %i[ show edit update destroy ]

  # GET /dummies or /dummies.json
  def index
    @dummies = Dummy.all
  end

  # GET /dummies/1 or /dummies/1.json
  def show
  end

  # GET /dummies/new
  def new
    @dummy = Dummy.new
  end

  # GET /dummies/1/edit
  def edit
  end

  # POST /dummies or /dummies.json
  def create
    @dummy = Dummy.new(dummy_params)

    respond_to do |format|
      if @dummy.save
        format.html { redirect_to dummy_url(@dummy), notice: "Dummy was successfully created." }
        format.json { render :show, status: :created, location: @dummy }
      else
        format.html { render :new, status: :unprocessable_entity }
        format.json { render json: @dummy.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /dummies/1 or /dummies/1.json
  def update
    respond_to do |format|
      if @dummy.update(dummy_params)
        format.html { redirect_to dummy_url(@dummy), notice: "Dummy was successfully updated." }
        format.json { render :show, status: :ok, location: @dummy }
      else
        format.html { render :edit, status: :unprocessable_entity }
        format.json { render json: @dummy.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /dummies/1 or /dummies/1.json
  def destroy
    @dummy.destroy

    respond_to do |format|
      format.html { redirect_to dummies_url, notice: "Dummy was successfully destroyed." }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_dummy
      @dummy = Dummy.find(params[:id])
    end

    # Only allow a list of trusted parameters through.
    def dummy_params
      params.fetch(:dummy, {})
    end
end
