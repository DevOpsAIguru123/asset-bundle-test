#!/bin/bash
# dbfs:/databricks/init/r-nexus-repo.sh

LOG_FILE="/databricks/driver/r-nexus-init.log"
echo "=== R Nexus init starting ===" >> "$LOG_FILE" 2>&1
echo "Env NEXUS_R_REPO = ${NEXUS_R_REPO}" >> "$LOG_FILE" 2>&1

NEXUS_URL="${NEXUS_R_REPO}"

if [[ -z "$NEXUS_URL" ]]; then
  echo "NEXUS_R_REPO is empty; leaving default CRAN mirror." >> "$LOG_FILE" 2>&1
  exit 0
fi

echo "Configuring R to use Nexus: $NEXUS_URL" >> "$LOG_FILE" 2>&1

# Create driver-level .Rprofile that R will auto-load
cat << EOF > /databricks/driver/.Rprofile
nexus <- Sys.getenv("NEXUS_R_REPO")
if (nzchar(nexus)) {
  options(repos = c(CRAN = nexus))
} else {
  # Fallback to default
  options(repos = c(CRAN = "https://cloud.r-project.org"))
}
EOF

# Also copy to root home so workers / non-interactive R sessions can see it
cp /databricks/driver/.Rprofile /root/.Rprofile 2>/dev/null || true

echo "R Nexus .Rprofile written." >> "$LOG_FILE" 2>&1