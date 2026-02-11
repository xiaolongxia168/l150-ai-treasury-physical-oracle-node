#!/bin/bash
# Autonomous skill installer
# Runs continuously to install useful skills

echo "🤖 Autonomous Skill Installer"
echo "Started: $(date)"
echo ""

SKILLS_TO_INSTALL=(
  # Monitoring & Alerting
  "speedtest"
  "opensysinfo"
  
  # Data & Analysis
  "financial-calculator"
  "quodd"
  
  # Security
  "skill-vetter"
  "flaw0"
  
  # Productivity
  "logseq"
  "pndr"
  "idea-coach"
  
  # Communication
  "discord"
  "mailchannels"
  
  # Development
  "perry-coding-agents"
  "openspec"
  "executing-plans"
  
  # Research
  "essence-distiller"
  "principle-synthesizer"
  "get-tldr"
  
  # Automation
  "joko-proactive-agent"
  "god-mode"
  "agent-config"
)

cd ~/.openclaw

for skill in "${SKILLS_TO_INSTALL[@]}"; do
  echo "Installing: $skill"
  npx clawhub@latest install "$skill" --force 2>&1 | tail -2
  echo ""
  sleep 2
done

echo ""
echo "✅ Batch installation complete"
echo "Total skills: $(ls ~/.openclaw/workspace/skills/ | wc -l)"
echo "Finished: $(date)"
