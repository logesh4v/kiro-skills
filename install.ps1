<#
.SYNOPSIS
  Install every skill in this repo into Kiro's skill directories.
.DESCRIPTION
  Default: junction-link into $env:USERPROFILE\.kiro\skills (IDE + CLI) and
  $env:USERPROFILE\.kiro\crew\skills (Crew). Re-running is safe.
    .\install.ps1              global install
    .\install.ps1 -Workspace   also link into .\.kiro\skills (needed for Kiro Web/Mobile)
    .\install.ps1 -Copy        copy instead of linking
  Update later with:  git pull
#>
param([switch]$Workspace, [switch]$Copy)
$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$KiroHome = if ($env:KIRO_HOME) { $env:KIRO_HOME } else { Join-Path $env:USERPROFILE ".kiro" }
$CrewHome = if ($env:KIROCREW_HOME) { $env:KIROCREW_HOME } else { Join-Path $env:USERPROFILE ".kiro\crew" }
$Targets = @((Join-Path $KiroHome "skills"), (Join-Path $CrewHome "skills"))
if ($Workspace) { $Targets += (Join-Path (Get-Location) ".kiro\skills") }

function Place($src, $dstDir) {
  New-Item -ItemType Directory -Force -Path $dstDir | Out-Null
  $dst = Join-Path $dstDir (Split-Path -Leaf $src)
  if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
  if ($Copy) { Copy-Item -Recurse $src $dst; Write-Host "  copy  $dst" }
  else { New-Item -ItemType Junction -Path $dst -Target $src | Out-Null; Write-Host "  link  $dst -> $src" }
}

Write-Host "kiro-skills installer ($(if ($Copy) {'copy'} else {'link'}))"
Get-ChildItem -Directory $Here | Where-Object { Test-Path (Join-Path $_.FullName "SKILL.md") } | ForEach-Object {
  Write-Host "$($_.Name):"
  foreach ($t in $Targets) { Place $_.FullName $t }
}
Write-Host "`nDone. Restart Kiro IDE/CLI (or start a new Crew chat). Invoke with /blog-writer."
