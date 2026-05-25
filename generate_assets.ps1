Add-Type -AssemblyName System.Drawing

$docsDir = "c:\Users\giand\Documents\segreti_scrittura\docs"
$artifactDir = "C:\Users\giand\.gemini\antigravity-ide\brain\4621d51c-3aa9-4f37-83c4-8cec26648acf"

# Copy generated images
$imagesMap = @{
    "copertina_matrix_1779736100842.png" = "copertina-matrix.jpg"
    "missione_matrix_1779736113808.png" = "missione-matrix.jpg"
    "metodo_matrix_1779736128574.png" = "metodo-matrix.jpg"
    "antico_testamento_1779736142515.png" = "sezione-antico-testamento.jpg"
    "nuovo_testamento_1779736166138.png" = "sezione-nuovo-testamento.jpg"
    "sezione_profeti_1779736178956.png" = "sezione-profeti.jpg"
    "sezione_vangeli_1779736192426.png" = "sezione-vangeli.jpg"
    "sezione_apocalisse_1779736205125.png" = "sezione-apocalisse.jpg"
}

foreach ($key in $imagesMap.Keys) {
    $src = Join-Path $artifactDir $key
    $dst = Join-Path $docsDir $imagesMap[$key]
    if (Test-Path $src) {
        $img = [System.Drawing.Image]::FromFile($src)
        $img.Save($dst, [System.Drawing.Imaging.ImageFormat]::Jpeg)
        $img.Dispose()
        Write-Host "Saved $dst"
    }
}

# Generate Backgrounds
$backgrounds = @(
    "sfondo-home.jpg", "sfondo-missione.jpg", "sfondo-metodo.jpg", 
    "sfondo-antico.jpg", "sfondo-nuovo.jpg", "sfondo-profeti.jpg", 
    "sfondo-vangeli.jpg", "sfondo-apocalisse.jpg"
)

$bgWidth = 1920
$bgHeight = 1080

foreach ($bg in $backgrounds) {
    $bmp = New-Object System.Drawing.Bitmap($bgWidth, $bgHeight)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.Clear([System.Drawing.Color]::FromArgb(5, 10, 5))
    
    $pen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(0, 30, 0), 1)
    for ($x = 0; $x -lt $bgWidth; $x += 100) { $g.DrawLine($pen, $x, 0, $x, $bgHeight) }
    for ($y = 0; $y -lt $bgHeight; $y += 100) { $g.DrawLine($pen, 0, $y, $bgWidth, $y) }
    
    $brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(0, 50, 0))
    $font = New-Object System.Drawing.Font("Consolas", 10)
    $rand = New-Object System.Random
    for ($i = 0; $i -lt 500; $i++) {
        $rx = $rand.Next(0, $bgWidth)
        $ry = $rand.Next(0, $bgHeight)
        $txt = $rand.Next(0, 2).ToString()
        $g.DrawString($txt, $font, $brush, $rx, $ry)
    }
    
    $dst = Join-Path $docsDir $bg
    $bmp.Save($dst, [System.Drawing.Imaging.ImageFormat]::Jpeg)
    $g.Dispose()
    $bmp.Dispose()
    Write-Host "Saved $dst"
}

# Generate Icons
$icons = @(
    "genesi", "esodo", "numeri", "giudici", "rut", "samuele", "re", 
    "esdra", "giobbe", "salmi", "proverbi", "cantico", "isaia", 
    "lamentazioni", "ezechiele", "daniele", "matteo", "giovanni", "atti"
)

$iconSize = 512

foreach ($icon in $icons) {
    $bmp = New-Object System.Drawing.Bitmap($iconSize, $iconSize)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.Clear([System.Drawing.Color]::Black)
    
    $penOuter = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(0, 255, 0), 5)
    $g.DrawRectangle($penOuter, 10, 10, 492, 492)
    
    $penInner = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(0, 150, 0), 3)
    $g.DrawLine($penInner, 256, 10, 502, 256)
    $g.DrawLine($penInner, 502, 256, 256, 502)
    $g.DrawLine($penInner, 256, 502, 10, 256)
    $g.DrawLine($penInner, 10, 256, 256, 10)
    
    $penCircle = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(0, 200, 0), 2)
    $g.DrawEllipse($penCircle, 156, 156, 200, 200)
    
    $brushNode = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(0, 255, 0))
    $penLine = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(0, 100, 0), 1)
    $rand = New-Object System.Random
    for ($i = 0; $i -lt 10; $i++) {
        $cx = $rand.Next(156, 356)
        $cy = $rand.Next(156, 356)
        $g.FillRectangle($brushNode, $cx, $cy, 10, 10)
        $g.DrawLine($penLine, 256, 256, $cx, $cy)
    }
    
    $dst = Join-Path $docsDir "$icon.png"
    $bmp.Save($dst, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $bmp.Dispose()
    Write-Host "Saved $dst"
}

Write-Host "All assets generated!"
