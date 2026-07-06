# Catalog inbox

Drop URLs (one per line, optional ` — note`) or fenced ```text blocks here, then run the drain (`/catalog-intake`). Blocked items are marked `⚠ needs-link` and stay until resolved.

```text
oossible tuning for local models

      "models": {
        "qwen3.6-35b-4bit": {
          "name": "Qwen3.6 35B",
          "reasoning": true,
          "limit": {
            "context": 65536,
            "output": 8192
          },
          "options": {
            "temperature": 0.6,
            "top_p": 0.95,
            "extraBody": {
              "max_tokens": 8192,
              "enable_thinking": true,
              "chat_template_kwargs": {
                "enable_thinking": true
              }
            }
          }
        }
      }

```text

To use Claude Code as your core harness, you can seamlessly swap back and forth between your cloud Claude subscription and Open Source Software (OSS) models (both local Ollama/LM Studio models and API-based external models).Because Claude Code natively routes traffic based on your terminal's environment variables, you can create quick command shortcuts to instantly switch your harness backend.Step 1: Fix a Critical Performance BugBefore switching to local models, you must fix a known bug in Claude Code. By default, Claude Code appends a changing "Attribution Header" to every prompt, which destroys your local model's KV Cache and slows down your inference by 90%.Add this to your environment file (~/.bashrc, ~/.zshrc, or windows profile):bashexport CLAUDE_CODE_ATTRIBUTION_HEADER=0
Use code with caution.Step 2: Configure Environment ShortcutsAdd the following aliases to your terminal profile (~/.zshrc or ~/.bashrc). This creates dedicated commands for your cloud subscription, local models, and third-party APIs.Option A: Your Claude Subscription / Official APITo use your paid Anthropic subscription/API limits, reset the variables back to defaults:bashalias claude-cloud='unset ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN ANTHROPIC_API_KEY; claude'
Use code with caution.Option B: Local OSS Models (via Ollama)Ensure your Ollama local model (like qwen3-coder or qwen3.5) has its context window manually expanded in Ollama's settings to at least 32k or 64k so the agent doesn't forget your files.bashalias claude-local='export ANTHROPIC_AUTH_TOKEN=ollama; export ANTHROPIC_BASE_URL=http://localhost:11434; claude --model qwen3.5'
Use code with caution.(If using LM Studio instead of Ollama, use http://localhost:1234 and export ANTHROPIC_AUTH_TOKEN=lmstudio.)Option C: Cloud OSS / API-Based Models (via OpenRouter or DeepSeek)If you want to use external open-source models hosted on API aggregators like OpenRouter, configure Claude Code to talk to their Anthropic-compatible endpoints:bashalias claude-oss-api='export ANTHROPIC_API_KEY="your-openrouter-key"; export ANTHROPIC_BASE_URL=https://openrouter.ai; claude --model deepseek/deepseek-coder'
Use code with caution.Step 3: Run Your HarnessOnce configured, reload your terminal (source ~/.zshrc). You can now change your entire backend harness instantly just by typing your chosen command:Type claude-cloud to use your paid Anthropic account.Type claude-local to run 100% offline and free using your computer's hardware.Type claude-oss-api to route through your third-party open-source API provider.


```