# Catalog inbox

Drop URLs (one per line, optional ` — note`) or fenced ```text blocks here, then run the drain (`/catalog-intake`). Blocked items are marked `⚠ needs-link` and stay until resolved.

https://github.com/e2b-dev/e2b
https://e2b.dev/docs
https://github.com/huggingface/smolagents
https://github.com/containers/bubblewrap
https://github.com/googlechromelabs/bubblewrap
https://github.com/blaxel-ai
https://blaxel.ai/

```text

Best practices for sandboxes
These key practices apply to Blaxel, E2B, and Docker sandboxes:

Resource management

Set memory and CPU limits
Implement execution timeouts
Monitor resource usage
Security

Run with minimal privileges
Disable unnecessary network access
Use environment variables for secrets
Environment

Keep dependencies minimal
Use fixed package versions
If you use base images, update them regularly
Cleanup

Cleanup

Always ensure proper cleanup of resources, especially for Docker containers, to avoid having dangling containers eating up resources.

Approach 1: Running just the code snippets in a sandbox
Pros:
Easier to set up with a simple parameter (executor_type="blaxel", executor_type="e2b", or executor_type="docker")
No need to transfer API keys to the sandbox
Better protection for your local environment
Fast execution with Blaxel’s hibernation technology (<25ms startup)
Cons:
Doesn’t support multi-agents (managed agents)
Still requires transferring state between your environment and the sandbox
Limited to specific code execution
Approach 2: Running the entire agentic system in a sandbox
Pros:
Supports multi-agents
Complete isolation of the entire agent system
More flexible for complex agent architectures
Cons:
Requires more manual setup
May require transferring sensitive API keys to the sandbox
Potentially higher latency due to more complex operations

Choose the approach that best balances your security needs with your application’s requirements. For most applications with simpler agent architectures, Approach 1 provides a good balance of security and ease of use. For more complex multi-agent systems where you need full isolation, Approach 2, while more involved to set up, offers better security guarantees

```