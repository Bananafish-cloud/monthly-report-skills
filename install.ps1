# monthly-report-skills 一键安装脚本
# 用法：
#   1. 下载仓库 ZIP 并解压
#   2. 右键 install.ps1 -> "使用 PowerShell 运行"
#      （或打开 PowerShell 执行：powershell -ExecutionPolicy Bypass -File install.ps1）
# 效果：把 monthly-report-skill-builder 复制到检测到的 agent 的 skills 目录

$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillDir = Join-Path $ScriptDir 'monthly-report-skill-builder'

if (-not (Test-Path $SkillDir)) {
    Write-Host "未找到 monthly-report-skill-builder 文件夹（应在 $SkillDir）" -ForegroundColor Red
    Write-Host "请确认 install.ps1 和 monthly-report-skill-builder 在同一个解压文件夹里。"
    Read-Host "按回车退出"
    exit 1
}

# 候选 agent 的 skills 目录（WorkBuddy 不同版本/机器可能用 .workbuddy 或 .hermes，都检测）
$Candidates = [ordered]@{
    'WorkBuddy (.workbuddy)' = Join-Path $HOME '.workbuddy\skills'
    'WorkBuddy (.hermes)'    = Join-Path $HOME '.hermes\skills'
    'Claude Code'            = Join-Path $HOME '.claude\skills'
}

$found = @()
foreach ($agent in $Candidates.Keys) {
    if (Test-Path $Candidates[$agent]) {
        $found += [pscustomobject]@{ Agent = $agent; Dir = $Candidates[$agent] }
    }
}

if ($found.Count -eq 0) {
    Write-Host "没检测到 WorkBuddy (~/.workbuddy/skills 或 ~/.hermes/skills) 或 Claude Code (~/.claude/skills)。" -ForegroundColor Yellow
    $manual = Read-Host "请输入你的 agent 的 skills 目录完整路径（或留空退出）"
    if ([string]::IsNullOrWhiteSpace($manual)) { Write-Host "已取消。"; exit 1 }
    $found = @([pscustomobject]@{ Agent = '自定义'; Dir = $manual })
}

foreach ($f in $found) {
    $target = Join-Path $f.Dir 'monthly-report-skill-builder'
    try {
        if (Test-Path $target) {
            Write-Host "检测到旧版本，覆盖更新 $($f.Agent) ..." -ForegroundColor Yellow
            Remove-Item $target -Recurse -Force
        }
        Copy-Item $SkillDir $target -Recurse -Force
        Write-Host "[OK] 已安装到 $($f.Agent): $target" -ForegroundColor Green
    } catch {
        Write-Host "[FAIL] 安装到 $($f.Agent) 失败: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "安装完成。注意：" -ForegroundColor Cyan
Write-Host "  1. 需要【新开一个对话/会话】，agent 才会重新加载 skills 列表并识别到它"
Write-Host "  2. 新会话里对 agent 说："
Write-Host '     「用 monthly-report-skill-builder 帮我生成 XX 项目月报的 Skill」'
Read-Host "按回车退出"
