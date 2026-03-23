#!/bin/bash
# Aider con DeepSeek (más rápido y preciso que Ollama local)

# Configurar API key (obtener en https://platform.deepseek.com/)
if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo "⚠️ Configura DEEPSEEK_API_KEY:"
    echo "export DEEPSEEK_API_KEY='tu-api-key-gratuita'"
    echo "Regístrate en: https://platform.deepseek.com/"
    exit 1
fi

# Configuración optimizada para DeepSeek
AIDER_OPTS=(
    --model "deepseek/deepseek-chat"  # Modelo estándar (más disponible)
    --yes                              # Auto-confirmar
    --auto-commits                     # Commits automáticos
    --no-git                          # Más rápido sin Git
)

echo "🚀 Aider con DeepSeek Coder (especializado en código)"
aider "${AIDER_OPTS[@]}" "$@"
