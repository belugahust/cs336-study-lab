$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Split-Path -Parent $PSScriptRoot)
$lessonNumber = Read-Host 'Lecture number (1-19)'
$sessionMinutes = Read-Host 'Minutes spent this session'
$sessionSummary = Read-Host 'What did you learn?'
$sessionQuestion = Read-Host 'Open question (optional)'
$videoDone = Read-Host 'Finished this lecture video? [y/N]'
$practiceDone = Read-Host 'Finished the exercise in lecture notes? [y/N]'
$pushNow = Read-Host 'Commit all project changes and push to GitHub? [y/N]'
$studyArgs = @('study.py', 'record', '--lecture', $lessonNumber, '--minutes', $sessionMinutes, '--summary', $sessionSummary, '--question', $sessionQuestion)
if ($videoDone -eq 'y') { $studyArgs += '--watched' }
if ($practiceDone -eq 'y') { $studyArgs += '--practice' }
if ($pushNow -eq 'y') { $studyArgs += @('--push', '--api') }
& python @studyArgs
exit $LASTEXITCODE
