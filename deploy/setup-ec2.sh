#!/usr/bin/env bash
# One-time setup for the CYPHER EC2 host (Ubuntu 24.04, t3.small or larger).
# Installs Docker, Jenkins, Python, AWS CLI v2 and a 2 GB swap file.
# Run once:  sudo bash setup-ec2.sh
set -euo pipefail

if [[ $EUID -ne 0 ]]; then echo "Run with sudo"; exit 1; fi

echo "==> Swap (keeps Jenkins + Docker builds from running out of memory)"
if ! swapon --show | grep -q /swapfile; then
  fallocate -l 2G /swapfile
  chmod 600 /swapfile
  mkswap /swapfile
  swapon /swapfile
  echo '/swapfile none swap sw 0 0' >> /etc/fstab
fi

echo "==> Base packages, Docker, Python, Java"
apt-get update -y
apt-get install -y ca-certificates curl unzip git fontconfig \
  docker.io python3 python3-venv python3-pip openjdk-21-jre

echo "==> AWS CLI v2"
if ! command -v aws >/dev/null; then
  curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-$(uname -m).zip" -o /tmp/awscliv2.zip
  unzip -q /tmp/awscliv2.zip -d /tmp
  /tmp/aws/install
fi

echo "==> Jenkins (LTS)"
install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key -o /etc/apt/keyrings/jenkins-keyring.asc
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" \
  > /etc/apt/sources.list.d/jenkins.list
apt-get update -y
apt-get install -y jenkins

echo "==> Let Jenkins use Docker; start everything on boot"
usermod -aG docker jenkins
usermod -aG docker ubuntu || true
systemctl enable --now docker
systemctl enable jenkins
systemctl restart jenkins

echo
echo "Done. Open http://<EC2-PUBLIC-DNS>:8080 and unlock Jenkins with:"
echo "  sudo cat /var/lib/jenkins/secrets/initialAdminPassword"
