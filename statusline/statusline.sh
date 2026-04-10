#!/bin/bash

# Claude Code Status Line — Context Window Usage Bar
# Shows: Model | Progress Bar | Percentage | Token Counts
#
# Install: copy to ~/.claude/statusline.sh and add to ~/.claude/settings.json
# Or run: statusline/install.sh from this repo

# Read JSON input from stdin
input=$(cat)

# Extract values
model=$(echo "$input" | jq -r '.model.display_name')
ctx_size=$(echo "$input" | jq -r '.context_window.context_window_size')

# Check if we have current_usage data (null before first API call)
has_usage=$(echo "$input" | jq -r '.context_window.current_usage != null')

if [ "$has_usage" = "true" ]; then
    input_tokens=$(echo "$input" | jq -r '.context_window.current_usage.input_tokens // 0')
    output_tokens=$(echo "$input" | jq -r '.context_window.current_usage.output_tokens // 0')
    cache_creation=$(echo "$input" | jq -r '.context_window.current_usage.cache_creation_input_tokens // 0')
    cache_read=$(echo "$input" | jq -r '.context_window.current_usage.cache_read_input_tokens // 0')

    # All four token categories occupy context window space
    total_used=$((input_tokens + output_tokens + cache_creation + cache_read))
    used=$(awk "BEGIN {printf \"%.1f\", ($total_used / $ctx_size) * 100}")
else
    total_used=0
    used="0.0"
fi

# Progress bar (20 chars wide, Unicode block characters)
bar_width=20
filled=$(awk "BEGIN {printf \"%.0f\", ($used / 100) * $bar_width}")

bar="["
for ((i=0; i<filled; i++)); do
    bar+="▓"
done
for ((i=filled; i<bar_width; i++)); do
    bar+="░"
done
bar+="]"

# Output with ANSI colors: cyan model, yellow %, green tokens
printf "\033[36m%s\033[0m | Context: %s \033[33m%s%%\033[0m | Tokens: \033[32m%s\033[0m/\033[32m%s\033[0m" \
    "$model" "$bar" "$used" "$total_used" "$ctx_size"
