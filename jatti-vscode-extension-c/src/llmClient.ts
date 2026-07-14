import * as vscode from "vscode";
import * as http from "http";
import * as https from "https";

/**
 * Jatti LLM Code Generator
 * Integrates with backend LLM server to generate Jatti code from English prompts
 */

export class JattiLLMClient {
  private apiUrl: string;
  private context: vscode.ExtensionContext;

  constructor(context: vscode.ExtensionContext, apiUrl: string = "https://jatti-llm-backend-production.up.railway.app") {
    this.context = context;
    this.apiUrl = apiUrl;
  }

  /**
   * Generate Jatti code from English prompt
   */
  async generateCode(prompt: string, selectedCode?: string): Promise<string | null> {
    try {
      // Show progress
      return await vscode.window.withProgress(
        {
          location: vscode.ProgressLocation.Notification,
          title: "Generating Jatti code...",
          cancellable: false,
        },
        async (progress) => {
          // Prepare context from selected code if available
          const context = selectedCode
            ? `Current code:\n${selectedCode}`
            : "Generate a complete Jatti program";

          const response = await this.makeRequest("/api/generate", {
            prompt,
            context,
            max_tokens: 1000,
          });

          if (!response.success) {
            throw new Error(response.error || "Failed to generate code");
          }

          return response.code;
        }
      );
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      vscode.window.showErrorMessage(`LLM Error: ${errorMsg}`);
      return null;
    }
  }

  /**
   * Validate generated Jatti code
   */
  async validateCode(code: string): Promise<{ valid: boolean; errors: string[] }> {
    try {
      const response = await this.makeRequest("/api/validate", { code });
      return {
        valid: response.valid,
        errors: response.errors || [],
      };
    } catch (error) {
      return {
        valid: false,
        errors: [`Validation error: ${error}`],
      };
    }
  }

  /**
   * Explain Jatti code in English
   */
  async explainCode(code: string): Promise<string | null> {
    try {
      return await vscode.window.withProgress(
        {
          location: vscode.ProgressLocation.Notification,
          title: "Analyzing code...",
          cancellable: false,
        },
        async () => {
          const response = await this.makeRequest("/api/explain", { code });
          return response.explanation || "Unable to generate explanation";
        }
      );
    } catch (error) {
      vscode.window.showErrorMessage(`Explanation error: ${error}`);
      return null;
    }
  }

  /**
   * Check if LLM server is running
   */
  async isServerReady(): Promise<boolean> {
    try {
      const response = await this.makeRequest("/health");
      return response.status === "ok";
    } catch {
      return false;
    }
  }

  /**
   * Make HTTP request to LLM server
   */
  private async makeRequest(endpoint: string, body?: any): Promise<any> {
    return new Promise((resolve, reject) => {
      const url = new URL(`${this.apiUrl}${endpoint}`);
      const isHttps = url.protocol === "https:";
      const client = isHttps ? https : http;

      const requestOptions = {
        method: body ? "POST" : "GET",
        hostname: url.hostname,
        port: url.port || (isHttps ? 443 : 80),
        path: url.pathname + url.search,
        headers: {
          "Content-Type": "application/json",
        },
      };

      const req = client.request(requestOptions, (res) => {
        let data = "";

        res.on("data", (chunk) => {
          data += chunk;
        });

        res.on("end", () => {
          try {
            const json = JSON.parse(data);
            if (res.statusCode && res.statusCode >= 200 && res.statusCode < 300) {
              resolve(json);
            } else {
              reject(new Error(json.error || `HTTP ${res.statusCode}`));
            }
          } catch (e) {
            reject(new Error(`Invalid JSON response: ${data}`));
          }
        });
      });

      req.on("error", reject);

      if (body) {
        req.write(JSON.stringify(body));
      }

      req.end();
    });
  }
}

/**
 * Register LLM commands with VS Code
 */
export function registerLLMCommands(context: vscode.ExtensionContext, llmClient: JattiLLMClient) {
  // Command: Generate Code from Prompt
  const generateCommand = vscode.commands.registerCommand("jatti.generateCode", async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage("No active editor");
      return;
    }

    // Get selected code if any
    const selectedCode = editor.document.getText(editor.selection);

    // Ask user for prompt
    const prompt = await vscode.window.showInputBox({
      placeHolder: 'Enter English description (e.g., "Create a function that adds two numbers")',
      title: "Jatti Code Generator",
      ignoreFocusOut: true,
    });

    if (!prompt) {
      return;
    }

    // Check server status
    const ready = await llmClient.isServerReady();
    if (!ready) {
      vscode.window.showErrorMessage(
        "LLM Server not running. Start it with: python scripts/llm_server.py"
      );
      return;
    }

    // Generate code
    const generatedCode = await llmClient.generateCode(prompt, selectedCode);
    if (!generatedCode) {
      return;
    }

    // Validate
    const validation = await llmClient.validateCode(generatedCode);
    if (!validation.valid) {
      const showResult = await vscode.window.showWarningMessage(
        `Generated code has issues:\n${validation.errors.join("\n")}`,
        "Insert Anyway",
        "Discard"
      );
      if (showResult !== "Insert Anyway") {
        return;
      }
    }

    // Insert code into editor
    const position = editor.selection.active;
    await editor.edit((editBuilder) => {
      editBuilder.insert(position, "\n" + generatedCode + "\n");
    });

    vscode.window.showInformationMessage("✅ Jatti code generated!");
  });

  // Command: Explain Code
  const explainCommand = vscode.commands.registerCommand("jatti.explainCode", async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage("No active editor");
      return;
    }

    // Get selected code or all code
    const code = editor.document.getText(editor.selection) || editor.document.getText();

    if (!code.trim()) {
      vscode.window.showInformationMessage("No code to explain");
      return;
    }

    // Check server status
    const ready = await llmClient.isServerReady();
    if (!ready) {
      vscode.window.showErrorMessage(
        "LLM Server not running. Start it with: python scripts/llm_server.py"
      );
      return;
    }

    // Explain code
    const explanation = await llmClient.explainCode(code);
    if (!explanation) {
      return;
    }

    // Show in output panel or message
    const webview = vscode.window.createWebviewPanel(
      "jattiExplanation",
      "Jatti Code Explanation",
      vscode.ViewColumn.Beside,
      {}
    );

    webview.webview.html = `
      <!DOCTYPE html>
      <html>
      <head>
        <style>
          body { font-family: Arial; padding: 20px; line-height: 1.6; }
          .explanation { background: #f5f5f5; padding: 15px; border-radius: 5px; }
          .code { background: #272822; color: #f8f8f2; padding: 15px; border-radius: 5px; font-family: monospace; overflow-x: auto; margin-bottom: 20px; }
        </style>
      </head>
      <body>
        <h2>Code Explanation</h2>
        <div class="explanation">
          ${explanation.replace(/\n/g, "<br>")}
        </div>
      </body>
      </html>
    `;
  });

  // Command: Refine Code (regenerate with additional context)
  const refineCommand = vscode.commands.registerCommand("jatti.refineCode", async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage("No active editor");
      return;
    }

    const refinement = await vscode.window.showInputBox({
      placeHolder: 'Describe how to refine the code (e.g., "Add error handling")',
      title: "Refine Generated Code",
      ignoreFocusOut: true,
    });

    if (!refinement) {
      return;
    }

    const currentCode = editor.document.getText(editor.selection);
    const prompt = `Refine this code: ${refinement}\n\nCurrent code:\n${currentCode}`;

    const refined = await llmClient.generateCode(prompt, currentCode);
    if (refined) {
      await editor.edit((editBuilder) => {
        editBuilder.replace(editor.selection, refined);
      });
    }
  });

  context.subscriptions.push(generateCommand, explainCommand, refineCommand);
}
