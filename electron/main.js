const { app, BrowserWindow, Menu, Tray, ipcMain, nativeImage } = require('electron');
const path = require('path');

let mainWindow;
let tray = null;
let isQuitting = false;

// Voorkom meerdere instanties
const gotTheLock = app.requestSingleInstanceLock();
if (!gotTheLock) {
    app.quit();
} else {
    app.on('second-instance', () => {
        if (mainWindow) {
            if (mainWindow.isMinimized()) mainWindow.restore();
            mainWindow.focus();
        }
    });
}

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        minWidth: 800,
        minHeight: 600,
        title: 'Tijdregistratie',
        icon: path.join(__dirname, '../assets/icon.png'),
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js')
        },
        show: false // Toon pas als geladen
    });

    // Laad de app
    mainWindow.loadFile('index.html');

    // Toon window wanneer klaar
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
    });

    // Minimaliseer naar tray in plaats van sluiten
    mainWindow.on('close', (event) => {
        if (!isQuitting) {
            event.preventDefault();
            mainWindow.hide();

            // Toon notificatie alleen de eerste keer (platform-specifiek)
            if (!app.isHidden) {
                const { Notification } = require('electron');
                if (process.platform === 'win32' && tray) {
                    // Windows: gebruik tray balloon
                    tray.displayBalloon({
                        title: 'Tijdregistratie',
                        content: 'De app draait nog op de achtergrond. Klik op het icoon om te openen.'
                    });
                } else if (Notification.isSupported()) {
                    // macOS/Linux: gebruik Notification API
                    new Notification({
                        title: 'Tijdregistratie',
                        body: 'De app draait nog op de achtergrond. Klik op het icoon om te openen.'
                    }).show();
                }
                app.isHidden = true;
            }
        }
        return false;
    });

    // Maak applicatie menu
    createMenu();
}

function createMenu() {
    const template = [
        {
            label: 'Bestand',
            submenu: [
                {
                    label: 'Exporteer naar CSV',
                    accelerator: 'CmdOrCtrl+E',
                    click: () => {
                        mainWindow.webContents.executeJavaScript('window.app && window.app.exportToCSV()');
                    }
                },
                { type: 'separator' },
                {
                    label: 'Afsluiten',
                    accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Alt+F4',
                    click: () => {
                        isQuitting = true;
                        app.quit();
                    }
                }
            ]
        },
        {
            label: 'Bewerken',
            submenu: [
                { label: 'Ongedaan maken', accelerator: 'CmdOrCtrl+Z', role: 'undo' },
                { label: 'Opnieuw', accelerator: 'Shift+CmdOrCtrl+Z', role: 'redo' },
                { type: 'separator' },
                { label: 'Knippen', accelerator: 'CmdOrCtrl+X', role: 'cut' },
                { label: 'Kopiëren', accelerator: 'CmdOrCtrl+C', role: 'copy' },
                { label: 'Plakken', accelerator: 'CmdOrCtrl+V', role: 'paste' }
            ]
        },
        {
            label: 'Beeld',
            submenu: [
                { label: 'Volledig scherm', accelerator: 'F11', role: 'togglefullscreen' },
                { type: 'separator' },
                { label: 'Inzoomen', accelerator: 'CmdOrCtrl+Plus', role: 'zoomIn' },
                { label: 'Uitzoomen', accelerator: 'CmdOrCtrl+-', role: 'zoomOut' },
                { label: 'Standaard zoom', accelerator: 'CmdOrCtrl+0', role: 'resetZoom' }
            ]
        },
        {
            label: 'Timer',
            submenu: [
                {
                    label: 'Start/Stop Timer',
                    accelerator: 'CmdOrCtrl+T',
                    click: () => {
                        mainWindow.webContents.executeJavaScript(`
                            if (window.app) {
                                if (window.app.timerRunning) {
                                    window.app.stopTimer();
                                } else {
                                    window.app.startTimer();
                                }
                            }
                        `);
                    }
                },
                {
                    label: 'Nieuw Project',
                    accelerator: 'CmdOrCtrl+N',
                    click: () => {
                        mainWindow.webContents.executeJavaScript('window.app && window.app.openProjectModal()');
                    }
                }
            ]
        },
        {
            label: 'Help',
            submenu: [
                {
                    label: 'Over Tijdregistratie',
                    click: () => {
                        const { dialog } = require('electron');
                        dialog.showMessageBox(mainWindow, {
                            type: 'info',
                            title: 'Over Tijdregistratie',
                            message: 'Tijdregistratie v1.0.0',
                            detail: 'Een gratis, open-source tijdregistratie app.\n\nGemaakt voor freelancers en kleine bedrijven.\n\nAlle data blijft lokaal op je computer.'
                        });
                    }
                }
            ]
        }
    ];

    // macOS specifieke aanpassingen
    if (process.platform === 'darwin') {
        template.unshift({
            label: app.getName(),
            submenu: [
                { label: 'Over Tijdregistratie', role: 'about' },
                { type: 'separator' },
                { label: 'Voorkeuren...', accelerator: 'Cmd+,', enabled: false },
                { type: 'separator' },
                { label: 'Verberg', accelerator: 'Cmd+H', role: 'hide' },
                { label: 'Verberg andere', accelerator: 'Cmd+Alt+H', role: 'hideOthers' },
                { type: 'separator' },
                {
                    label: 'Stop Tijdregistratie',
                    accelerator: 'Cmd+Q',
                    click: () => {
                        isQuitting = true;
                        app.quit();
                    }
                }
            ]
        });
    }

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
}

function createTray() {
    // Maak een simpel icoon (16x16 pixels)
    const iconPath = path.join(__dirname, '../assets/tray-icon.png');

    // Fallback naar een basis icoon als het bestand niet bestaat
    let trayIcon;
    try {
        trayIcon = nativeImage.createFromPath(iconPath);
        if (trayIcon.isEmpty()) {
            trayIcon = createDefaultIcon();
        }
    } catch (e) {
        trayIcon = createDefaultIcon();
    }

    tray = new Tray(trayIcon);
    tray.setToolTip('Tijdregistratie');

    const contextMenu = Menu.buildFromTemplate([
        {
            label: 'Open Tijdregistratie',
            click: () => {
                mainWindow.show();
            }
        },
        { type: 'separator' },
        {
            label: 'Start Timer',
            click: () => {
                mainWindow.show();
                mainWindow.webContents.executeJavaScript('window.app && window.app.startTimer()');
            }
        },
        {
            label: 'Stop Timer',
            click: () => {
                mainWindow.webContents.executeJavaScript('window.app && window.app.stopTimer()');
            }
        },
        { type: 'separator' },
        {
            label: 'Afsluiten',
            click: () => {
                isQuitting = true;
                app.quit();
            }
        }
    ]);

    tray.setContextMenu(contextMenu);

    tray.on('click', () => {
        if (mainWindow.isVisible()) {
            mainWindow.hide();
        } else {
            mainWindow.show();
        }
    });

    tray.on('double-click', () => {
        mainWindow.show();
    });
}

function createDefaultIcon() {
    // Maak een simpel standaard icoon
    const size = process.platform === 'darwin' ? 22 : 16;
    const canvas = nativeImage.createEmpty();
    return canvas;
}

// App lifecycle
app.whenReady().then(() => {
    createWindow();
    createTray();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        } else {
            mainWindow.show();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('before-quit', () => {
    isQuitting = true;
});

// IPC handlers voor communicatie met renderer
ipcMain.handle('get-app-version', () => {
    return app.getVersion();
});

ipcMain.handle('show-notification', (event, title, body) => {
    const { Notification } = require('electron');
    if (Notification.isSupported()) {
        new Notification({ title, body }).show();
    }
});
