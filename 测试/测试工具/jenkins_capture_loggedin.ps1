Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class JenkinsWindowCapture {
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT rect);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int command);
  [DllImport("user32.dll")] public static extern void keybd_event(byte virtualKey, byte scanCode, uint flags, UIntPtr extraInfo);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }
}
'@

$imageDir = Join-Path $PSScriptRoot 'images'
$chrome = Get-Process chrome | Where-Object { $_.MainWindowTitle -like '*Jenkins*' } | Select-Object -First 1
if (-not $chrome) { throw '没有找到已登录的 Jenkins Chrome 窗口' }

$shell = New-Object -ComObject WScript.Shell
[JenkinsWindowCapture]::ShowWindow($chrome.MainWindowHandle, 3) | Out-Null
[JenkinsWindowCapture]::SetForegroundWindow($chrome.MainWindowHandle) | Out-Null

function Save-CurrentJenkinsWindow([string]$fileName) {
  Start-Sleep -Seconds 4
  $rect = New-Object JenkinsWindowCapture+RECT
  [JenkinsWindowCapture]::GetWindowRect($chrome.MainWindowHandle, [ref]$rect) | Out-Null
  $width = $rect.Right - $rect.Left
  $height = $rect.Bottom - $rect.Top
  $path = Join-Path $imageDir $fileName
  $bitmap = New-Object System.Drawing.Bitmap($width, $height)
  $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
  $graphics.CopyFromScreen($rect.Left, $rect.Top, 0, 0, $bitmap.Size)
  $bitmap.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
  $graphics.Dispose()
  $bitmap.Dispose()
  Write-Output $path
}

function Open-And-Capture([string]$url, [string]$fileName) {
  [JenkinsWindowCapture]::SetForegroundWindow($chrome.MainWindowHandle) | Out-Null
  Start-Sleep -Milliseconds 300
  $shell.AppActivate($chrome.Id) | Out-Null
  [System.Windows.Forms.Clipboard]::SetText($url)
  [JenkinsWindowCapture]::keybd_event(0x11, 0, 0, [UIntPtr]::Zero)
  [JenkinsWindowCapture]::keybd_event(0x4C, 0, 0, [UIntPtr]::Zero)
  [JenkinsWindowCapture]::keybd_event(0x4C, 0, 2, [UIntPtr]::Zero)
  [JenkinsWindowCapture]::keybd_event(0x11, 0, 2, [UIntPtr]::Zero)
  Start-Sleep -Milliseconds 200
  [JenkinsWindowCapture]::keybd_event(0x11, 0, 0, [UIntPtr]::Zero)
  [JenkinsWindowCapture]::keybd_event(0x56, 0, 0, [UIntPtr]::Zero)
  [JenkinsWindowCapture]::keybd_event(0x56, 0, 2, [UIntPtr]::Zero)
  [JenkinsWindowCapture]::keybd_event(0x11, 0, 2, [UIntPtr]::Zero)
  Start-Sleep -Milliseconds 200
  [JenkinsWindowCapture]::keybd_event(0x0D, 0, 0, [UIntPtr]::Zero)
  [JenkinsWindowCapture]::keybd_event(0x0D, 0, 2, [UIntPtr]::Zero)
  Start-Sleep -Seconds 3
  Save-CurrentJenkinsWindow $fileName
}

Save-CurrentJenkinsWindow 'jenkins-workspace-current.png'
Open-And-Capture 'http://localhost:8088/manage/' 'jenkins-manage-current.png'
Open-And-Capture 'http://localhost:8088/manage/pluginManager/' 'jenkins-plugins-current.png'
Open-And-Capture 'http://localhost:8088/manage/configure' 'jenkins-system-current.png'
Open-And-Capture 'http://localhost:8088/manage/configureTools/' 'jenkins-tools-current.png'
