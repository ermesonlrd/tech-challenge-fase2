#!/bin/bash

# COMANDO="python main-compare.py"
COMANDO="python main.py"

for i in {1..5}; do
    LOGFILE="simulacao_${i}.log"
    echo "Executando main.py (execução $i)..."
    
    START_TIME=$(date +%s)
    $COMANDO > "$LOGFILE" 2>&1
    END_TIME=$(date +%s)
    
    DURATION=$((END_TIME - START_TIME))
    
    # Insere o tempo no início do log
    sed -i "1iTempo de execução: ${DURATION} segundos\n" "$LOGFILE"
done

