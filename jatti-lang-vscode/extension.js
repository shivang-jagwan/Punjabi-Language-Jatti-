const vscode = require('vscode');
const { execFile } = require('child_process');
const path = require('path');
const fs = require('fs');

// Output channel for showing messages
let outputChannel;

function resolvePythonAndCli(filePath) {
    const config = vscode.workspace.getConfiguration('jatti');
    const pythonPath = config.get('pythonPath') || 'python';
    const cliPathSetting = (config.get('cliPath') || '').trim();

    const candidates = [];

    if (cliPathSetting) {
        if (cliPathSetting.toLowerCase().endsWith('.py')) {
            candidates.push(cliPathSetting);
        } else {
            candidates.push(path.join(cliPathSetting, 'cli.py'));
        }
    }

    // Current behavior: cli.py next to the file
    const fileDir = path.dirname(filePath);
    candidates.push(path.join(fileDir, 'cli.py'));

    // Common setup: cli.py at workspace root
    const folders = vscode.workspace.workspaceFolders || [];
    for (const folder of folders) {
        candidates.push(path.join(folder.uri.fsPath, 'cli.py'));
    }

    const cliPath = candidates.find(p => p && fs.existsSync(p));
    if (!cliPath) {
        return {
            pythonPath,
            cliPath: null,
            error: 'Could not find cli.py. Set Settings → Jatti → Cli Path (jatti.cliPath) to your Jatti install folder or cli.py file.'
        };
    }

    return { pythonPath, cliPath, error: null };
}

function activate(context) {
    console.log('Jatti Language Extension activated!');
    
    // Create output channel
    outputChannel = vscode.window.createOutputChannel('Jatti');
    
    // Register Run command
    let runCommand = vscode.commands.registerCommand('jatti.run', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No file open');
            return;
        }
        
        const filePath = editor.document.fileName;
        
        // Check if it's a .jatti file
        if (!filePath.endsWith('.jatti')) {
            vscode.window.showErrorMessage('This is not a Jatti file (.jatti)');
            return;
        }
        
        runJattiFile(filePath);
    });
    
    // Register Run in Terminal command
    let runTerminalCommand = vscode.commands.registerCommand('jatti.runInTerminal', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No file open');
            return;
        }
        
        const filePath = editor.document.fileName;
        
        if (!filePath.endsWith('.jatti')) {
            vscode.window.showErrorMessage('This is not a Jatti file (.jatti)');
            return;
        }
        
        runInTerminal(filePath);
    });
    
    // Register Build command
    let buildCommand = vscode.commands.registerCommand('jatti.build', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No file open');
            return;
        }
        
        const filePath = editor.document.fileName;
        
        if (!filePath.endsWith('.jatti')) {
            vscode.window.showErrorMessage('This is not a Jatti file (.jatti)');
            return;
        }
        
        buildJattiFile(filePath);
    });
    
    // Register Format command
    let formatCommand = vscode.commands.registerCommand('jatti.format', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No file open');
            return;
        }
        
        const filePath = editor.document.fileName;
        
        if (!filePath.endsWith('.jatti')) {
            vscode.window.showErrorMessage('This is not a Jatti file (.jatti)');
            return;
        }
        
        formatJattiFile(filePath);
    });
    
    context.subscriptions.push(runCommand);
    context.subscriptions.push(runTerminalCommand);
    context.subscriptions.push(buildCommand);
    context.subscriptions.push(formatCommand);
}

function runJattiFile(filePath) {
    outputChannel.clear();
    outputChannel.show(true);
    outputChannel.append(`⏳ Running: ${path.basename(filePath)}\n`);
    outputChannel.append(`📁 Path: ${filePath}\n`);
    outputChannel.append('━'.repeat(50) + '\n\n');

    const { pythonPath, cliPath, error } = resolvePythonAndCli(filePath);
    if (error) {
        outputChannel.append(`❌ ${error}\n`);
        vscode.window.showErrorMessage(error);
        return;
    }

    const process = execFile(pythonPath, [cliPath, 'run', filePath], {
        cwd: path.dirname(cliPath),
        maxBuffer: 10 * 1024 * 1024
    }, (error, stdout, stderr) => {
        if (stdout) outputChannel.append(stdout);
        if (stderr) outputChannel.append(stderr);
        outputChannel.append('\n' + '━'.repeat(50) + '\n');
        
        if (error && error.code !== 0) {
            outputChannel.append(`❌ Execution failed with code ${error.code}\n`);
            vscode.window.showErrorMessage(`❌ Execution failed (exit code: ${error.code})`);
        } else {
            outputChannel.append('✅ Execution completed successfully!\n');
            vscode.window.showInformationMessage('✅ Jatti file executed successfully!');
        }
    });
}

function runInTerminal(filePath) {
    const terminal = vscode.window.createTerminal('Jatti');
    terminal.show();

    const { pythonPath, cliPath, error } = resolvePythonAndCli(filePath);
    if (error) {
        vscode.window.showErrorMessage(error);
        return;
    }

    // Run using absolute paths so it works from any folder/shell
    terminal.sendText(`"${pythonPath}" "${cliPath}" run "${filePath}"`);
}

function buildJattiFile(filePath) {
    outputChannel.clear();
    outputChannel.show(true);
    outputChannel.append(`🔨 Building: ${path.basename(filePath)}\n`);
    outputChannel.append('━'.repeat(50) + '\n\n');
    
    const { pythonPath, cliPath, error } = resolvePythonAndCli(filePath);
    if (error) {
        outputChannel.append(`❌ ${error}\n`);
        vscode.window.showErrorMessage(error);
        return;
    }

    execFile(pythonPath, [cliPath, 'build', filePath], {
        cwd: path.dirname(cliPath),
        maxBuffer: 10 * 1024 * 1024
    }, (error, stdout, stderr) => {
        if (stdout) outputChannel.append(stdout);
        if (stderr) outputChannel.append(stderr);
        outputChannel.append('\n' + '━'.repeat(50) + '\n');
        
        if (error && error.code !== 0) {
            outputChannel.append(`❌ Build failed with code ${error.code}\n`);
            vscode.window.showErrorMessage(`Build failed (exit code: ${error.code})`);
        } else {
            const pythonFile = filePath.replace('.jatti', '.py');
            outputChannel.append(`✅ Build completed! Created: ${path.basename(pythonFile)}\n`);
            vscode.window.showInformationMessage(`✅ Built to ${path.basename(pythonFile)}`);
        }
    });
}

function formatJattiFile(filePath) {
    outputChannel.clear();
    outputChannel.show(true);
    outputChannel.append(`📝 Formatting: ${path.basename(filePath)}\n`);
    outputChannel.append('━'.repeat(50) + '\n\n');
    
    const { pythonPath, cliPath, error } = resolvePythonAndCli(filePath);
    if (error) {
        outputChannel.append(`❌ ${error}\n`);
        vscode.window.showErrorMessage(error);
        return;
    }

    execFile(pythonPath, [cliPath, 'format', filePath], {
        cwd: path.dirname(cliPath),
        maxBuffer: 10 * 1024 * 1024
    }, (error, stdout, stderr) => {
        if (stdout) outputChannel.append(stdout);
        if (stderr) outputChannel.append(stderr);
        outputChannel.append('\n' + '━'.repeat(50) + '\n');
        
        if (error && error.code !== 0) {
            outputChannel.append(`❌ Format failed with code ${error.code}\n`);
            vscode.window.showErrorMessage(`Format failed (exit code: ${error.code})`);
        } else {
            outputChannel.append('✅ Format completed!\n');
            vscode.window.showInformationMessage('✅ File formatted!');
        }
    });
}

function deactivate() {
    if (outputChannel) {
        outputChannel.dispose();
    }
}

module.exports = {
    activate,
    deactivate
};
