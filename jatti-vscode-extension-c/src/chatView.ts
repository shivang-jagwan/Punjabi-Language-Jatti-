import * as vscode from 'vscode';
import { JattiLLMClient } from './llmClient';

export class ChatViewProvider implements vscode.WebviewViewProvider {
  public static readonly viewType = 'jatti.chatView';
  private _view?: vscode.WebviewView;

  constructor(
    private readonly _extensionUri: vscode.Uri,
    private readonly _llmClient: JattiLLMClient
  ) {}

  public resolveWebviewView(
    webviewView: vscode.WebviewView,
    context: vscode.WebviewViewResolveContext,
    _token: vscode.CancellationToken,
  ) {
    this._view = webviewView;
    webviewView.webview.options = {
      enableScripts: true,
      localResourceRoots: [this._extensionUri]
    };

    webviewView.webview.html = this._getHtmlForWebview();

    webviewView.webview.onDidReceiveMessage(async (data) => {
      switch (data.type) {
        case 'generate':
          {
            const prompt = data.value;
            if (!prompt) return;

            // Check if server is ready
            const ready = await this._llmClient.isServerReady();
            if (!ready) {
              webviewView.webview.postMessage({
                type: 'error',
                value: 'LLM Server is not running. Please start the backend.'
              });
              return;
            }

            // Get selected code if any to provide as context
            let selectedCode = '';
            const editor = vscode.window.activeTextEditor;
            if (editor) {
              selectedCode = editor.document.getText(editor.selection);
            }

            try {
              const code = await this._llmClient.generateCode(prompt, selectedCode);
              if (code) {
                webviewView.webview.postMessage({
                  type: 'response',
                  value: code
                });
              } else {
                webviewView.webview.postMessage({
                  type: 'error',
                  value: 'Failed to generate code.'
                });
              }
            } catch (err: any) {
              webviewView.webview.postMessage({
                type: 'error',
                value: err.message
              });
            }
            break;
          }
        case 'insertAtCursor':
          {
            const editor = vscode.window.activeTextEditor;
            if (editor) {
              editor.edit(editBuilder => {
                editBuilder.insert(editor.selection.active, data.value);
              });
            }
            break;
          }
      }
    });
  }

  private _getHtmlForWebview() {
    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jatti AI Assistant</title>
  <style>
    body {
      font-family: var(--vscode-font-family);
      color: var(--vscode-editor-foreground);
      background-color: var(--vscode-editor-background);
      padding: 10px;
      display: flex;
      flex-direction: column;
      height: 100vh;
      box-sizing: border-box;
    }
    #chat-container {
      flex: 1;
      overflow-y: auto;
      margin-bottom: 10px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .message {
      padding: 8px 12px;
      border-radius: 6px;
      line-height: 1.4;
      word-wrap: break-word;
    }
    .user-msg {
      background-color: var(--vscode-button-background);
      color: var(--vscode-button-foreground);
      align-self: flex-end;
      max-width: 85%;
    }
    .ai-msg {
      background-color: var(--vscode-editorWidget-background);
      border: 1px solid var(--vscode-widget-border);
      align-self: flex-start;
      width: 100%;
      box-sizing: border-box;
    }
    .error-msg {
      color: var(--vscode-errorForeground);
      font-weight: bold;
    }
    pre {
      background: var(--vscode-textCodeBlock-background);
      padding: 8px;
      border-radius: 4px;
      overflow-x: auto;
      margin: 5px 0;
    }
    code {
      font-family: var(--vscode-editor-font-family);
      font-size: 0.9em;
    }
    .action-btn {
      background: var(--vscode-button-secondaryBackground, transparent);
      color: var(--vscode-textLink-foreground);
      border: none;
      cursor: pointer;
      font-size: 0.9em;
      padding: 2px 4px;
      margin-top: 5px;
      text-decoration: underline;
    }
    .action-btn:hover {
      color: var(--vscode-textLink-activeForeground);
    }
    .input-container {
      display: flex;
      flex-direction: column;
      gap: 5px;
      margin-bottom: 10px;
    }
    textarea {
      width: 100%;
      background: var(--vscode-input-background);
      color: var(--vscode-input-foreground);
      border: 1px solid var(--vscode-input-border);
      padding: 8px;
      border-radius: 4px;
      box-sizing: border-box;
      resize: vertical;
      font-family: inherit;
    }
    textarea:focus {
      outline: 1px solid var(--vscode-focusBorder);
      border-color: transparent;
    }
    button.primary {
      background: var(--vscode-button-background);
      color: var(--vscode-button-foreground);
      border: none;
      padding: 8px;
      border-radius: 4px;
      cursor: pointer;
      font-weight: bold;
    }
    button.primary:hover {
      background: var(--vscode-button-hoverBackground);
    }
    button:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  </style>
</head>
<body>
  <div id="chat-container">
    <div class="message ai-msg">
      Hello! I'm your Jatti AI Assistant powered by Qwen 2.5 and Semantic RAG. How can I help you write Jatti code today?
    </div>
  </div>
  
  <div class="input-container">
    <textarea id="prompt-input" rows="3" placeholder="Describe the Jatti code you want to generate..."></textarea>
    <button id="generate-btn" class="primary">Generate Code</button>
  </div>

  <script>
    const vscode = acquireVsCodeApi();
    
    const chatContainer = document.getElementById('chat-container');
    const promptInput = document.getElementById('prompt-input');
    const generateBtn = document.getElementById('generate-btn');

    function appendMessage(type, content) {
      const msgDiv = document.createElement('div');
      msgDiv.className = 'message ' + type;
      msgDiv.innerHTML = content;
      chatContainer.appendChild(msgDiv);
      chatContainer.scrollTop = chatContainer.scrollHeight;
      return msgDiv;
    }

    generateBtn.addEventListener('click', () => {
      const text = promptInput.value.trim();
      if (!text) return;

      appendMessage('user-msg', text);
      promptInput.value = '';
      
      const loadingDiv = appendMessage('ai-msg', 'Generating code... (this may take a few seconds)');
      loadingDiv.id = 'loading-indicator';
      
      generateBtn.disabled = true;
      vscode.postMessage({ type: 'generate', value: text });
    });

    window.addEventListener('message', event => {
      const message = event.data;
      const loadingDiv = document.getElementById('loading-indicator');
      if (loadingDiv) loadingDiv.remove();
      
      generateBtn.disabled = false;

      if (message.type === 'response') {
        const rawCode = message.value;
        
        function highlightJatti(code) {
          const keywords = ['sun_we', 'ja_we', 'je', 'nahin_taan_je', 'nahin_taan', 'jadon_tak', 'har_ek', 'roko_oye_roko', 'chalo_oye_chalo', 'chal_koshish_karle', 'pakad', 'wapas_kar', 'kaam', 'chal_oye', 'ban'];
          const builtins = ['chilla_we', 'range_banao', 'kinna_lamba', 'kism', 'likh', 'padh', 'ganao', 'sab_ton_vaddha', 'sab_ton_chhota', 'sorted', 'reversed', 'vada_likha', 'chhota_likha', 'saf_karo', 'vand_karo', 'badal_de', 'shuru_hunda', 'khatam_hunda', 'dhundh_ja'];
          const booleans = ['sach', 'jhoot', 'khaali'];
          
          let h = code.replace(/</g, '&lt;').replace(/>/g, '&gt;');
          
          // Comments MUST be first so it doesn't match the '#' in our CSS hex colors!
          h = h.replace(/(#.*)$/gm, '<span style="color: #6a9955;">$1</span>');
          
          // Strings
          h = h.replace(/(["'])(.*?)\\1/g, '<span style="color: #ce9178;">$&</span>');
          // Keywords
          const kwRegex = new RegExp('\\\\b(' + keywords.join('|') + ')\\\\b', 'g');
          h = h.replace(kwRegex, '<span style="color: #c586c0;">$1</span>');
          // Builtins
          const biRegex = new RegExp('\\\\b(' + builtins.join('|') + ')\\\\b', 'g');
          h = h.replace(biRegex, '<span style="color: #dcdcaa;">$1</span>');
          // Booleans
          const boolRegex = new RegExp('\\\\b(' + booleans.join('|') + ')\\\\b', 'g');
          h = h.replace(boolRegex, '<span style="color: #569cd6;">$1</span>');
          // Numbers
          h = h.replace(/\\b(\\d+(\\.\\d+)?)\\b/g, '<span style="color: #b5cea8;">$1</span>');
          
          return h;
        }

        const highlightedCode = highlightJatti(rawCode);
        const html = \`
          <div>Here is the generated code:</div>
          <pre><code>\${highlightedCode}</code></pre>
          <button class="action-btn" onclick="insertCode(this)">Insert at Cursor</button>
        \`;
        
        const msg = appendMessage('ai-msg', html);
        msg.dataset.code = rawCode;
      } else if (message.type === 'error') {
        appendMessage('ai-msg', \`<span class="error-msg">Error: \${message.value}</span>\`);
      }
    });

    window.insertCode = function(btn) {
      const rawCode = btn.parentElement.dataset.code;
      vscode.postMessage({ type: 'insertAtCursor', value: rawCode });
    };
  </script>
</body>
</html>`;
  }
}
