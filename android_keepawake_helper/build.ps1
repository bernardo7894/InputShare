$ErrorActionPreference = "Stop"

function Invoke-Checked {
    & $args[0] @($args[1..($args.Count - 1)])
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed: $($args -join ' ')"
    }
}

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ProjectDir
$SdkDir = $env:ANDROID_SDK_ROOT
if (-not $SdkDir) { $SdkDir = $env:ANDROID_HOME }
if (-not $SdkDir) { $SdkDir = Join-Path $env:LOCALAPPDATA "Android\Sdk" }

$BuildToolsDir = Join-Path $SdkDir "build-tools\35.0.1"
$PlatformJar = Join-Path $SdkDir "platforms\android-35\android.jar"
$OutDir = Join-Path $ProjectDir "build"
$ClassesDir = Join-Path $OutDir "classes"
$DexDir = Join-Path $OutDir "dex"
$UnsignedApk = Join-Path $OutDir "InputShareKeepAwake-unsigned.apk"
$AlignedApk = Join-Path $OutDir "InputShareKeepAwake-aligned.apk"
$ApkPath = Join-Path $RootDir "server\InputShareKeepAwake.apk"
$KeystorePath = Join-Path $OutDir "debug.keystore"

New-Item -ItemType Directory -Path $OutDir, $ClassesDir, $DexDir -Force | Out-Null
Remove-Item -Path (Join-Path $ClassesDir "*") -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path (Join-Path $DexDir "*") -Recurse -Force -ErrorAction SilentlyContinue

Invoke-Checked (Join-Path $BuildToolsDir "aapt2.exe") compile --dir (Join-Path $ProjectDir "res") -o (Join-Path $OutDir "res.zip")
Invoke-Checked (Join-Path $BuildToolsDir "aapt2.exe") link `
    -I $PlatformJar `
    --manifest (Join-Path $ProjectDir "AndroidManifest.xml") `
    -o $UnsignedApk `
    (Join-Path $OutDir "res.zip")

Invoke-Checked "javac" -source 1.8 -target 1.8 -bootclasspath $PlatformJar -d $ClassesDir `
    (Join-Path $ProjectDir "src\com\inputshare\keepawake\KeepAwakeService.java")
Invoke-Checked (Join-Path $BuildToolsDir "d8.bat") --lib $PlatformJar --output $DexDir (Join-Path $ClassesDir "com\inputshare\keepawake\KeepAwakeService.class")

Add-Type -AssemblyName System.IO.Compression.FileSystem
$apkZip = [System.IO.Compression.ZipFile]::Open($UnsignedApk, "Update")
try {
    $existingDex = $apkZip.GetEntry("classes.dex")
    if ($existingDex) { $existingDex.Delete() }
    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
        $apkZip,
        (Join-Path $DexDir "classes.dex"),
        "classes.dex"
    ) | Out-Null
} finally {
    $apkZip.Dispose()
}

Invoke-Checked (Join-Path $BuildToolsDir "zipalign.exe") -f 4 $UnsignedApk $AlignedApk
if (-not (Test-Path $KeystorePath)) {
    Invoke-Checked "keytool" -genkeypair `
        -keystore $KeystorePath `
        -storepass android `
        -keypass android `
        -alias androiddebugkey `
        -keyalg RSA `
        -keysize 2048 `
        -validity 10000 `
        -dname "CN=Android Debug,O=Android,C=US"
}
Invoke-Checked (Join-Path $BuildToolsDir "apksigner.bat") sign `
    --ks $KeystorePath `
    --ks-pass pass:android `
    --key-pass pass:android `
    --out $ApkPath `
    $AlignedApk

Write-Host "Built $ApkPath"
