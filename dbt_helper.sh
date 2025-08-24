#!/bin/bash

# Fix permissions on dbt directory
fix_permissions() {
  echo "Fixing permissions on dbt directory..."
  docker exec dbt_container chmod -R 777 /root/dbt
  echo "Permissions fixed!"
}

# Function to create a directory in the dbt models folder
create_dbt_dir() {
  if [ -z "$1" ]; then
    echo "Please provide a directory name"
    exit 1
  fi
  
  echo "Creating directory: models/$1"
  docker exec dbt_container mkdir -p /root/dbt/my_project/models/$1
  docker exec dbt_container chmod -R 777 /root/dbt/my_project/models/$1
  echo "Directory created: models/$1"
}

# Function to create a SQL model file
create_dbt_model() {
  if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Please provide directory and model name"
    echo "Usage: $0 create_model directory_name model_name 'SQL content'"
    exit 1
  fi
  
  dir_path="/root/dbt/my_project/models/$1"
  file_name="$2.sql"
  content="${3:-"-- Default model template\nSELECT * FROM weather_data.weather_data"}"
  
  echo "Creating model file: $dir_path/$file_name"
  # Use printf to ensure newlines are preserved
  docker exec -i dbt_container bash -c "mkdir -p $dir_path && printf \"$content\" > $dir_path/$file_name && chmod 777 $dir_path/$file_name"
  echo "Model file created: $dir_path/$file_name"
}

# Function to create a schema.yml file for documentation
create_schema_yml() {
  if [ -z "$1" ]; then
    echo "Please provide a directory name"
    echo "Usage: $0 create_schema directory_name"
    exit 1
  fi
  
  dir_path="/root/dbt/my_project/models/$1"
  schema_content="version: 2

models:
  - name: example_model
    description: \"An example model\"
    columns:
      - name: id
        description: \"The primary key\"
        tests:
          - unique
          - not_null"
  
  echo "Creating schema.yml file in: $dir_path"
  docker exec -i dbt_container bash -c "mkdir -p $dir_path && echo \"$schema_content\" > $dir_path/schema.yml && chmod 777 $dir_path/schema.yml"
  echo "schema.yml created: $dir_path/schema.yml"
}

# Help function
show_help() {
  echo "DBT Helper Script"
  echo "Usage: $0 <command> [arguments]"
  echo ""
  echo "Commands:"
  echo "  fix_permissions                      Fix permissions on the dbt directory"
  echo "  create_dir <directory_name>          Create a new directory in models"
  echo "  create_model <dir> <name> [content]  Create a new SQL model file"
  echo "  create_schema <directory_name>       Create a schema.yml file in directory"
  echo "  run_models <directory_name>          Run dbt models in specified directory"
  echo "  run_specific <model_name>            Run a specific model"
  echo "  list_models                          List all available models"
  echo ""
}

# Function to run models in a specific directory
run_models() {
  if [ -z "$1" ]; then
    model_path="+"  # Run all models
  else
    model_path="+models/$1"
  fi
  
  echo "Running dbt models: $model_path"
  docker exec -i dbt_container bash -c "cd /root/dbt/my_project && dbt run --select $model_path"
}

# Function to run a specific model
run_specific() {
  if [ -z "$1" ]; then
    echo "Please provide a model name"
    exit 1
  fi
  
  echo "Running dbt model: $1"
  docker exec -i dbt_container bash -c "cd /root/dbt/my_project && dbt run --select $1"
}

# Function to list all models
list_models() {
  echo "Listing all dbt models:"
  docker exec -i dbt_container bash -c "cd /root/dbt/my_project && find models -name '*.sql' | sort"
}

# Main execution
case "$1" in
  fix_permissions)
    fix_permissions
    ;;
  create_dir)
    create_dbt_dir "$2"
    ;;
  create_model)
    create_dbt_model "$2" "$3" "$4"
    ;;
  create_schema)
    create_schema_yml "$2"
    ;;
  run_models)
    run_models "$2"
    ;;
  run_specific)
    run_specific "$2"
    ;;
  list_models)
    list_models
    ;;
  *)
    show_help
    ;;
esac
