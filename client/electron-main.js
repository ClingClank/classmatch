const { app, BrowserWindow } = require('electron')
const path = require('path')
const isDev = !app.isPackaged

function createWindow() {
  const win = new BrowserWindow({
    width: 1100,
    height: 800,
    webPreferences: { nodeIntegration: false }
  })
  const devUrl = 'http://localhost:5173'
  const prodUrl = 'file://' + path.join(__dirname, 'dist', 'index.html')
  win.loadURL(isDev ? devUrl : prodUrl)
}

app.whenReady().then(() => {
  createWindow()
  app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow() })
})
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit() })
