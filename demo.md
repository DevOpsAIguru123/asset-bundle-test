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

# Helper to write Rprofile.site if a given etc dir exists
write_rprofile_site() {
  local etc_dir="$1"
  if [[ -d "$etc_dir" ]]; then
    echo "Writing ${etc_dir}/Rprofile.site" >> "$LOG_FILE" 2>&1
    cat << EOF > "${etc_dir}/Rprofile.site"
local({
  options(
    repos = c(
      CRAN = "${NEXUS_URL}"
    )
  )
})
EOF
  else
    echo "Directory ${etc_dir} does not exist, skipping." >> "$LOG_FILE" 2>&1
  fi
}

# 1) Use the R_HOME from this environment (what your notebook reports)
R_HOME=$(R RHOME 2>/dev/null || true)
echo "Detected R_HOME = ${R_HOME}" >> "$LOG_FILE" 2>&1
if [[ -n "$R_HOME" ]]; then
  write_rprofile_site "${R_HOME}/etc"
fi

# 2) Also try the common Databricks paths, just in case
write_rprofile_site "/usr/lib/R/etc"
write_rprofile_site "/databricks/spark/R/lib/R/etc"

# 3) User-level .Rprofile as a backup
cat << EOF > /root/.Rprofile
local({
  options(
    repos = c(
      CRAN = "${NEXUS_URL}"
    )
  )
})
EOF
cp /root/.Rprofile /databricks/driver/.Rprofile 2>/dev/null || true
echo "Wrote /root/.Rprofile and /databricks/driver/.Rprofile" >> "$LOG_FILE" 2>&1

echo "=== R Nexus init finished ===" >> "$LOG_FILE" 2>&1