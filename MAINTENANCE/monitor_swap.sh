#!/bin/bash
# monitor_swap.sh - Monitoreo Swap antiX
# Si RAM sistema > 10240MB → loguear alerta en hypothetical_growth.log

# Umbrales
RAM_WARNING_MB=10240  # 10GB
RAM_CRITICAL_MB=11264  # 11GB
LOG_FILE="$(dirname "$0")/hypothetical_growth.log"

# Función de logging
log_alert() {
    local level="$1"
    local ram_mb="$2"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    echo "--- ALERTA ANTIX ($level) ---" >> "$LOG_FILE"
    echo "Timestamp: $timestamp" >> "$LOG_FILE"
    echo "RAM_Sistema: ${ram_mb}MB" >> "$LOG_FILE"
    echo "Umbral: ${level}_UMBRAL (${RAM_WARNING_MB}MB)" >> "$LOG_FILE"
    echo "Acción: Monitoreo activado - posible desborde" >> "$LOG_FILE"
    echo "Estado: ALERTA_SISTEMA" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
}

# Obtener RAM actual (Linux)
get_ram_usage() {
    if command -v free >/dev/null 2>&1; then
        # Usar free (Linux estándar)
        local ram_kb=$(free | grep '^Mem:' | awk '{print $3}')
        echo $((ram_kb / 1024))
    elif command -v vm_stat >/dev/null 2>&1; then
        # macOS alternativa
        local ram_pages=$(vm_stat | grep "Pages free:" | awk '{print $3}' | sed 's/\.//')
        echo $((ram_pages * 4096 / 1024 / 1024))
    else
        echo "0"
    fi
}

# Monitoreo principal
monitor_ram() {
    local current_ram=$(get_ram_usage)
    
    if [ "$current_ram" -gt "$RAM_CRITICAL_MB" ]; then
        log_alert "CRITICAL" "$current_ram"
        return 2
    elif [ "$current_ram" -gt "$RAM_WARNING_MB" ]; then
        log_alert "WARNING" "$current_ram"
        return 1
    else
        return 0
    fi
}

# Modo de operación
case "${1:-monitor}" in
    "monitor")
        monitor_ram
        ;;
    "continuous")
        # Modo continuo (para cron)
        echo "Iniciando monitoreo continuo de RAM..."
        while true; do
            monitor_ram
            sleep 300  # 5 minutos
        done
        ;;
    "test")
        # Modo prueba
        echo "Modo prueba - simulando umbrales:"
        echo "RAM actual: $(get_ram_usage)MB"
        echo "Umbral WARNING: ${RAM_WARNING_MB}MB"
        echo "Umbral CRITICAL: ${RAM_CRITICAL_MB}MB"
        monitor_ram
        ;;
    "status")
        # Estado del sistema
        current_ram=$(get_ram_usage)
        echo "Estado RAM: ${current_ram}MB / 12288MB"
        echo "Porcentaje: $(( current_ram * 100 / 12288 ))%"
        
        if [ "$current_ram" -gt "$RAM_CRITICAL_MB" ]; then
            echo "Estado: CRITICAL - Desborde inminente"
        elif [ "$current_ram" -gt "$RAM_WARNING_MB" ]; then
            echo "Estado: WARNING - Acercándose al límite"
        else
            echo "Estado: OK - Sistema estable"
        fi
        ;;
    *)
        echo "Uso: $0 [monitor|continuous|test|status]"
        echo "  monitor    - Verifica RAM actual (default)"
        echo "  continuous - Monitoreo continuo (para cron cada 5 min)"
        echo "  test       - Modo prueba con estado actual"
        echo "  status     - Estado completo del sistema"
        exit 1
        ;;
esac
