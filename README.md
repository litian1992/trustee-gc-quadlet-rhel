# Trustee Guest Components Quadlet - RHEL Integration
Run Trustee guest components (AA, CDH, ASR) as systemd-managed containers on RHEL using Podman Quadlet.

## Installation
```bash
# Install the package
dnf install trustee-gc-quadlet

# Pull the container image
podman pull quay.io/litian/trustee-gc:latest

# Configure
vi /etc/trustee-gc/aa/config.toml
vi /etc/trustee-gc/cdh/config.toml

# Start services
systemctl start trustee-gc-aa
systemctl start trustee-gc-cdh
systemctl start trustee-gc-asr
```

## Building RPM
