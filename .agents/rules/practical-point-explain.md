# Practical Point Explain Rule

Whenever the user asks to explain a command, flag, CLI output, config file, script, or practical step (from `practical/` or any DevOps/cloud/Docker/Kubernetes workflow):

1. **Always save or update a Markdown explanation file** inside `/home/shumon/Documents/coding-practice/practical-point-explain/` with a clear, descriptive kebab-case filename (e.g., `kind-config-yaml.md`, `docker-run-production-hardening.md`).
2. **Match the established format:**
   - Clear title (`# ...`).
   - **At the very top (right under the title & source file):** Include a `## Short Summary (TL;DR)` section covering:
     - **What this file does**
     - **Why it is needed**
     - **Real-world production example**
     - **All important details / key takeaways**
   - Include the exact command or file snippet being explained.
   - Break down **every single line, key, value, and flag** one by one, explaining:
     - **What each key and value means** (e.g., for `kind: Namespace`, explain both `kind` and `Namespace`)
     - **Real-world production example** for each item
     - **What happens without it** (or common gotchas)
3. **Update existing files** in `practical-point-explain/` if the user asks follow-up questions on the same topic, instead of creating duplicates.
4. **Also include the `Short Summary (TL;DR)` at the top of your chat reply** (covering what it does, why it's needed, real-world production example, and key details) before giving the line-by-line breakdown.
