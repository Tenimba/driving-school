# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 2023_06_02_214241) do

  create_table "active_storage_attachments", force: :cascade do |t|
    t.string "name", null: false
    t.string "record_type", null: false
    t.bigint "record_id", null: false
    t.bigint "blob_id", null: false
    t.datetime "created_at", null: false
    t.index ["blob_id"], name: "index_active_storage_attachments_on_blob_id"
    t.index ["record_type", "record_id", "name", "blob_id"], name: "index_active_storage_attachments_uniqueness", unique: true
  end

  create_table "active_storage_blobs", force: :cascade do |t|
    t.string "key", null: false
    t.string "filename", null: false
    t.string "content_type"
    t.text "metadata"
    t.string "service_name", null: false
    t.bigint "byte_size", null: false
    t.string "checksum", null: false
    t.datetime "created_at", null: false
    t.index ["key"], name: "index_active_storage_blobs_on_key", unique: true
  end

  create_table "active_storage_variant_records", force: :cascade do |t|
    t.bigint "blob_id", null: false
    t.string "variation_digest", null: false
    t.index ["blob_id", "variation_digest"], name: "index_active_storage_variant_records_uniqueness", unique: true
  end

  create_table "decisions", force: :cascade do |t|
    t.integer "etape_id", null: false
    t.string "action"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.boolean "is_questionnaire"
    t.index ["etape_id"], name: "index_decisions_on_etape_id"
  end

  create_table "elements", force: :cascade do |t|
    t.integer "quete_id", null: false
    t.string "image"
    t.integer "force"
    t.integer "vie"
    t.integer "xpplus"
    t.integer "element_type"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["quete_id"], name: "index_elements_on_quete_id"
  end

  create_table "elements_users", force: :cascade do |t|
    t.integer "user_id", null: false
    t.integer "element_id", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["element_id"], name: "index_elements_users_on_element_id"
    t.index ["user_id"], name: "index_elements_users_on_user_id"
  end

  create_table "etables", force: :cascade do |t|
    t.integer "quete_id", null: false
    t.string "image"
    t.integer "force"
    t.integer "vie"
    t.integer "xpplus"
    t.string "type"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["quete_id"], name: "index_etables_on_quete_id"
  end

  create_table "etapes", force: :cascade do |t|
    t.string "titre"
    t.text "description"
    t.integer "quete_id", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.string "type"
    t.integer "xp"
    t.boolean "termine"
    t.index ["quete_id"], name: "index_etapes_on_quete_id"
  end

  create_table "personnages", force: :cascade do |t|
    t.string "nom"
    t.integer "niveau"
    t.integer "vie"
    t.integer "force"
    t.integer "agilite"
    t.integer "intelligence"
    t.integer "charisme"
    t.integer "chance"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.integer "xp"
    t.integer "endurance"
  end

  create_table "player_game_masters", force: :cascade do |t|
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.integer "player_id"
    t.integer "game_master_id"
    t.index ["game_master_id"], name: "index_player_game_masters_on_game_master_id"
    t.index ["player_id"], name: "index_player_game_masters_on_player_id"
  end

  create_table "pnjs", force: :cascade do |t|
    t.integer "vie"
    t.integer "force"
    t.string "avatar"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.string "nom"
    t.integer "etape_id"
    t.integer "quete_id"
    t.index ["etape_id"], name: "index_pnjs_on_etape_id"
    t.index ["quete_id"], name: "index_pnjs_on_quete_id"
  end

  create_table "questions", force: :cascade do |t|
    t.string "title"
    t.text "content"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.integer "etape_id", null: false
    t.index ["etape_id"], name: "index_questions_on_etape_id"
  end

  create_table "quetes", force: :cascade do |t|
    t.string "titre"
    t.text "description"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.integer "game_master_id"
  end

  create_table "reponses", force: :cascade do |t|
    t.text "contenu"
    t.boolean "correcte"
    t.integer "question_id", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["question_id"], name: "index_reponses_on_question_id"
  end

  create_table "terminers", force: :cascade do |t|
    t.integer "user_id", null: false
    t.integer "quete_id", null: false
    t.integer "etape_id", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["etape_id"], name: "index_terminers_on_etape_id"
    t.index ["quete_id"], name: "index_terminers_on_quete_id"
    t.index ["user_id"], name: "index_terminers_on_user_id"
  end

  create_table "users", force: :cascade do |t|
    t.string "email", default: "", null: false
    t.string "encrypted_password", default: "", null: false
    t.string "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.datetime "remember_created_at"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.string "role"
    t.integer "vie"
    t.integer "force"
    t.string "name"
    t.integer "xp"
    t.index ["email"], name: "index_users_on_email", unique: true
    t.index ["reset_password_token"], name: "index_users_on_reset_password_token", unique: true
  end

  create_table "users_elements", id: false, force: :cascade do |t|
    t.integer "user_id"
    t.integer "element_id"
    t.index ["element_id"], name: "index_users_elements_on_element_id"
    t.index ["user_id"], name: "index_users_elements_on_user_id"
  end

  add_foreign_key "active_storage_attachments", "active_storage_blobs", column: "blob_id"
  add_foreign_key "active_storage_variant_records", "active_storage_blobs", column: "blob_id"
  add_foreign_key "decisions", "etapes"
  add_foreign_key "elements", "quetes"
  add_foreign_key "elements_users", "elements"
  add_foreign_key "elements_users", "users"
  add_foreign_key "etables", "quetes"
  add_foreign_key "etapes", "quetes"
  add_foreign_key "player_game_masters", "users", column: "game_master_id"
  add_foreign_key "player_game_masters", "users", column: "player_id"
  add_foreign_key "pnjs", "etapes"
  add_foreign_key "pnjs", "quetes"
  add_foreign_key "questions", "etapes"
  add_foreign_key "reponses", "questions"
  add_foreign_key "terminers", "etapes"
  add_foreign_key "terminers", "quetes"
  add_foreign_key "terminers", "users"
end
