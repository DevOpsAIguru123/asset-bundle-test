#!/bin/bash
# /dbfs/databricks/init/r-nexus-repo.sh
# Dynamically inject Nexus URL into Rprofile.site using Spark env variable.

# Pull Nexus URL from Spark environment
NEXUS_URL="${NEXUS_R_REPO}"

# Fallback if not set
if [[ -z "$NEXUS_URL" ]]; then
  echo "WARNING: NEXUS_R_REPO is not set. R will use default CRAN mirror."
  exit 0
fi

echo "Configuring R to use Nexus CRAN repo: $NEXUS_URL"

# Create Rprofile.site on driver
cat << EOF > /databricks/driver/Rprofile.site
options(
  repos = c(
    CRAN = "$NEXUS_URL"
  )
)
EOF

# Copy to worker nodes as well
cp /databricks/driver/Rprofile.site /usr/lib/R/etc/Rprofile.site 2>/dev/null || true
cp /databricks/driver/Rprofile.site /databricks/spark/R/lib/R/etc/Rprofile.site 2>/dev/null || true