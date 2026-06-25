# AGENTS.md

- 使用中文 Discord 指令名稱時，請用 `@bot.command(name="...")` 綁定中文名稱。
- Python 函式名稱建議保留英文（如 `choujoukyuu`），並用 `aliases` 提供中文指令（如 `超上級`）與英文備援。
- 避免把中文文字直接寫在 `def` 名稱上，避免編碼/輸出環境異常。
