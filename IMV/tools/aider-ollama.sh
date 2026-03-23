#!/bin/bash
# Aider optimizado para Ollama local

# Configuración para 12GB RAM
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_NUM_PARALLEL=1

# Usar modelo rápido y ligero con formato ollama/
MODEL="ollama/qwen2.5:0.5b"

# Configuración de Aider para velocidad (solo argumentos válidos)
AIDER_OPTS=(
    --model "$MODEL"
    --yes                    # Auto-confirmar cambios
    --no-git                # Sin operaciones Git (más rápido)
    --auto-commits          # Commitear automáticamente
)

# Iniciar Aider con configuración optimizada
echo "🚀 Iniciando Aider con Ollama $MODEL (optimizado para 12GB RAM)"
aider "${AIDER_OPTS[@]}" "$@"
