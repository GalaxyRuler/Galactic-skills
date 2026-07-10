param(
  [Parameter(Mandatory=$true)]
  [string]$Main,
  [ValidateSet("pdf", "xelatex", "lualatex")]
  [string]$Engine = "pdf",
  [switch]$AllowShellEscape
)
if (!(Test-Path -LiteralPath $Main)) {
  Write-Error "Main .tex file not found: $Main"
  exit 2
}
$engineFlag = switch ($Engine) {
  "pdf" { "-pdf" }
  "xelatex" { "-pdfxe" }
  "lualatex" { "-pdflua" }
}
$args = @(
  $engineFlag,
  "-interaction=nonstopmode",
  "-halt-on-error",
  "-file-line-error"
)
if ($AllowShellEscape) {
  Write-Warning "shell escape explicitly enabled by user."
  $args += "-shell-escape"
}
$args += $Main
& latexmk @args
exit $LASTEXITCODE
