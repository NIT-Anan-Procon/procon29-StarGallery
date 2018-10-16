"use strct";

const electron = require('electron');
// import electron from "electron"; // ES6 以下 var の使用を禁止
const app = electron.app; // コントロールモジュール
const BrowserWindow = electron.BrowserWindow; //ウインドウの生成モジュール
let mainWindow = null;

app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('ready', function () {

    const { spawn } = require('child_process');
    const pytest = spawn('python', ['./arduino/test.py']);

    mainWindow = new BrowserWindow({ width: 800, height: 600 });
    mainWindow.loadURL('file://' + __dirname + '/index.html');

    mainWindow.on('closed', function () {
        mainWindow = null;
        pytest.kill('SIGINT');
    });
});
