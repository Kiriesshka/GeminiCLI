#!/bin/bash

# Настройки
userName="USER"
aiName="GEMINI"
memoryDeep=10
memory=()
models=("gemini-1.0-pro" "gemini-1.5-pro" "gemini-1.5-flash")
model="${models[2]}"
API_KEY=""
PROMPTS_DIR="./PROMPTS"

# Цвета
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CYAN='\033[96m'
RESET='\033[0m'

load_prompt() {
    local name="$1"
    memory=()
    if [[ -f "$PROMPTS_DIR/$name" ]]; then
        local text
        text=$(<"$PROMPTS_DIR/$name")
        memory+=("$text")
        echo -e "${CYAN}PROMPT:${RESET}\n    > $text"
    else
        echo -e "${RED}SYSTEM:${RESET} Error! Prompt file not found or inaccessible."
    fi

    if [[ -f "$PROMPTS_DIR/$name.settings" ]]; then
        IFS="_/_" read -r aiName userName <"$PROMPTS_DIR/$name.settings"
    else
        echo -e "${RED}SYSTEM:${RESET} Error! Prompt settings file not found or inaccessible."
    fi
}

make_question() {
    local text="MEMORY: $memory CURRENT MESSAGE TO YOU(RESPOND ON IT): $question"
    local q="$1"
    local mem="${memory[*]}"
    local url="https://generativelanguage.googleapis.com/v1beta/models/$model:generateContent?key=$API_KEY"
    local payload=$(jq -n \
        --arg memory "$mem" \
        --arg question "$q" \
	--arg text "$text" \
        '{
            contents: [{"parts": [{"text": $text}]}],
            safetySettings: [
                {category: "HARM_CATEGORY_HARASSMENT", threshold: "BLOCK_NONE"},
                {category: "HARM_CATEGORY_HATE_SPEECH", threshold: "BLOCK_NONE"},
                {category: "HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold: "BLOCK_NONE"},
                {category: "HARM_CATEGORY_DANGEROUS_CONTENT", threshold: "BLOCK_NONE"}
            ]
        }')

    response=$(curl -s -X POST -H "Content-Type: application/json" -d "$payload" "$url")
    if [[ $? -eq 0 ]]; then
        local message=$(echo "$response" | jq -r '.candidates[0].content.parts[0].text' 2>/dev/null)
        if [[ -n "$message" ]]; then
            echo -e "${GREEN}$aiName:${RESET}\n    > $message"
            memory+=("$userName: $q" "$aiName: $message")
            if [[ ${#memory[@]} -gt $memoryDeep ]]; then
                memory=("${memory[@]:1}")
            fi
        else
            echo -e "${RED}SYSTEM:${RESET} Error in response!"
        fi
    else
        echo -e "${RED}SYSTEM:${RESET} Request failed."
    fi
}

show_help() {
    echo -e "${CYAN}SYSTEM:${RESET} Commands:"
    echo "  /help                  - Show this help"
    echo "  /stop                  - Stop the program"
    echo "  /memory                - Show current AI memory"
    echo "  /clear                 - Clear all memory"
    echo "  /username [name]       - Set new username"
    echo "  /ainame [name]         - Set new AI name"
    echo "  /load [filename]       - Load prompt from file"
    echo "  /switch [index]        - Switch model by index"
    echo "  /info                  - Show AI info"
    echo "  /save [filename]       - Save dialogue to file"
    echo "  /memorydeep [number]   - Set memory depth"
}

run_program=true
while $run_program; do
    echo -ne "${YELLOW}$userName:${RESET}\n    > "
    read -r question
    if [[ "$question" == /* ]]; then
        case "$question" in
        "/help")
            show_help
            ;;
        "/stop")
            run_program=false
            ;;
        "/memory")
            echo -e "${CYAN}SYSTEM:${RESET} Memory:"
            for m in "${memory[@]}"; do
                echo "  $m"
            done
            ;;
        "/clear")
            memory=()
            ;;
        "/username "*)
            userName="${question#* }"
            ;;
        "/ainame "*)
            aiName="${question#* }"
            ;;
        "/load "*)
            load_prompt "${question#* }"
            ;;
        "/switch "*)
            if [[ "${question#* }" =~ ^[0-9]+$ ]]; then
                model="${models[${question#* }]}"
                echo -e "${CYAN}SYSTEM:${RESET} Switched to [$model]"
            else
                echo -e "${CYAN}SYSTEM:${RESET} Models:"
                for i in "${!models[@]}"; do
                    echo "  [$i]: ${models[$i]}"
                done
            fi
            ;;
        "/info")
            echo -e "${CYAN}SYSTEM:${RESET} Info"
            echo "  Current model: $model"
            echo "  Memory: ${#memory[@]}/$memoryDeep"
            ;;
        "/save "*)
            local file="${question#* }"
            printf "%s\n" "${memory[@]}" >"$file"
            echo -e "${CYAN}SYSTEM:${RESET} Saved to [$file]"
            ;;
        "/memorydeep "*)
            memoryDeep="${question#* }"
            echo -e "${CYAN}SYSTEM:${RESET} Set memory depth to [$memoryDeep]"
            ;;
        *)
            echo -e "${RED}SYSTEM:${RESET} Unknown command."
            ;;
        esac
    else
        make_question "$question"
    fi
done

