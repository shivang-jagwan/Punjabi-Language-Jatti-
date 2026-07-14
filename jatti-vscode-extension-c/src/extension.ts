import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { spawn } from 'child_process';
import { JattiLLMClient, registerLLMCommands } from './llmClient';
import { ChatViewProvider } from './chatView';

const KEYWORDS = [
  'sun_we', 'ja_we', 'chal_oye', 'ban', 'chilla_we',
  'je', 'nahin_taan_je', 'nahin_taan', 'har_ek', 'jadon_tak',
  'roko_oye_roko', 'chalo_oye_chalo', 'kaam', 'wapas_kar',
  'chal_koshish_karle', 'pakad', 'vadha_hai', 'nikka_hai',
  'barabar', 'barabar_nahi_hai', 'vadha_ya_barabar', 'nikka_ya_barabar',
  'sach', 'jhoot', 'khaali', 'ate', 'ya_te', 'nahi', 'te'
];

const BUILTINS = [
  'range_banao', 'kinna_lamba', 'kism', 'likh', 'padh',
  'ganao', 'sab_ton_vaddha', 'sab_ton_chhota', 'sorted', 'reversed',
  'vada_likha', 'chhota_likha', 'saf_karo', 'vand_karo', 'badal_de', 'shuru_hunda', 'khatam_hunda', 'dhundh_ja'
];

let jattiOutputChannel: vscode.OutputChannel;

export function activate(context: vscode.ExtensionContext) {
  jattiOutputChannel = vscode.window.createOutputChannel('Jatti');
  
  // Initialize LLM Client
  const llmServerUrl = vscode.workspace.getConfiguration('jatti').get<string>('llmServerUrl') || "https://jatti-llm-backend-production.up.railway.app";
  const llmClient = new JattiLLMClient(context, llmServerUrl);
  registerLLMCommands(context, llmClient);
  
  // Register the AI Assistant Sidebar
  const chatProvider = new ChatViewProvider(context.extensionUri, llmClient);
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider(ChatViewProvider.viewType, chatProvider)
  );
  
  const runDisposable = vscode.commands.registerCommand('jatti.runFile', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage('Open a .jatti file first.');
      return;
    }

    if (editor.document.languageId !== 'jatti') {
      vscode.window.showErrorMessage('Active file is not a Jatti file.');
      return;
    }

    if (editor.document.isUntitled) {
      const saved = await editor.document.save();
      if (!saved) {
        vscode.window.showErrorMessage('Save the file before running.');
        return;
      }
    } else if (editor.document.isDirty) {
      await editor.document.save();
    }

    const filePath = editor.document.fileName;
    const runtimePath = resolveRuntimePath(context);

    if (!runtimePath) {
      vscode.window.showErrorMessage('Jatti runtime not found. Put jatti.exe at extension runtime/win32/jatti.exe or set jatti.runtimePath.');
      return;
    }

    jattiOutputChannel.clear();
    jattiOutputChannel.show(true);
    jattiOutputChannel.appendLine(`Running: ${filePath}\n`);

    try {
      const jattiProcess = spawn(runtimePath, ['run', filePath]);
      
      jattiProcess.stdout.on('data', (data) => {
        jattiOutputChannel.append(data.toString());
      });

      jattiProcess.stderr.on('data', (data) => {
        jattiOutputChannel.append(data.toString());
      });

      jattiProcess.on('close', (code) => {
        if (code === 0) {
          jattiOutputChannel.appendLine('\\n✅ Execution complete');
        } else {
          jattiOutputChannel.appendLine(`\\n❌ Execution failed with code ${code}`);
        }
      });

      jattiProcess.on('error', (err) => {
        jattiOutputChannel.appendLine(`\\n❌ Failed to start process: ${err.message}`);
      });
    } catch (error: any) {
      jattiOutputChannel.appendLine(`\\n❌ Execution failed: ${error.message}`);
    }
  });

  const completionDisposable = vscode.languages.registerCompletionItemProvider(
    { language: 'jatti' },
    {
      provideCompletionItems() {
        const keywordItems = KEYWORDS.map((word) => {
          const item = new vscode.CompletionItem(word, vscode.CompletionItemKind.Keyword);
          item.insertText = word;
          return item;
        });

        const builtinItems = BUILTINS.map((name) => {
          const item = new vscode.CompletionItem(name, vscode.CompletionItemKind.Function);
          item.insertText = `${name}`;
          return item;
        });

        return [...keywordItems, ...builtinItems];
      }
    }
  );

  context.subscriptions.push(runDisposable, completionDisposable);
}

export function deactivate() {
  if (jattiOutputChannel) {
    jattiOutputChannel.dispose();
  }
}

function resolveRuntimePath(context: vscode.ExtensionContext): string | undefined {
  const configured = vscode.workspace.getConfiguration('jatti').get<string>('runtimePath')?.trim();
  if (configured && fs.existsSync(configured)) {
    return configured;
  }

  if (process.platform === 'win32') {
    const workspaceRuntime = path.resolve(context.extensionPath, '..', 'c', 'bin', 'jatti.exe');
    if (fs.existsSync(workspaceRuntime)) {
      return workspaceRuntime;
    }

    const bundled = path.join(context.extensionPath, 'runtime', 'win32', 'jatti.exe');
    if (fs.existsSync(bundled)) {
      return bundled;
    }
  }

  return undefined;
}
