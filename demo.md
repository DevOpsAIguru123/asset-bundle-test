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

echo "Using Nexus URL: $NEXUS_URL" >> "$LOG_FILE" 2>&1

# R HOME (for the R used by notebooks)
R_HOME=$(R RHOME 2>/dev/null || true)
echo "Detected R_HOME = ${R_HOME}" >> "$LOG_FILE" 2>&1

ETC_DIR="${R_HOME}/etc"
if [[ -d "$ETC_DIR" ]]; then
  echo "Writing ${ETC_DIR}/Rprofile.site" >> "$LOG_FILE" 2>&1

  # This runs on every R session start, AFTER all startup scripts
  cat << 'EOF' > "${ETC_DIR}/Rprofile.site"
nexus_repo <- Sys.getenv("NEXUS_R_REPO")

if (nzchar(nexus_repo)) {
  .First <- function() {
    # This executes after R has started, overriding any earlier repo setting
    options(repos = c(CRAN = nexus_repo))
  }
}
EOF
else
  echo "ETC_DIR ${ETC_DIR} does not exist, skipping Rprofile.site." >> "$LOG_FILE" 2>&1
fi

# Also write user-level .Rprofile as a backup
cat << 'EOF' > /root/.Rprofile
nexus_repo <- Sys.getenv("NEXUS_R_REPO")

if (nzchar(nexus_repo)) {
  .First <- function() {
    options(repos = c(CRAN = nexus_repo))
  }
}
EOF

cp /root/.Rprofile /databricks/driver/.Rprofile 2>/dev/null || true
echo "Wrote /root/.Rprofile and /databricks/driver/.Rprofile" >> "$LOG_FILE" 2>&1
echo "=== R Nexus init finished ===" >> "$LOG_FILE" 2>&1