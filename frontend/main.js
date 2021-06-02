const{app, BrowserWindow} = require('electron')


//cannot be called before ready 
function createWindow() {
  const mainWindow= new BrowserWindow({
    width:800,
    height: 600
  })
  
  mainWindow.loadFile('index.html')

}

//promise to close
app.whenReady().then(() => {
  createWindow()
  
  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

//quitting the app when all windows are closed (win & linux only)
app.on('window-all-closed', function () {
  if(process.platform !== 'darwin') app.quit
})

