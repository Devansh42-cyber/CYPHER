# Setup Guide — step by step (for Dev)

Region used everywhere: **ap-south-1 (Mumbai)**. If you pick another, change `AWS_REGION` in the `Jenkinsfile`.
📸 = take a screenshot for DEVOPS.md (save to `docs/screenshots/`).

---

## Day 1 — Git (Task 1)

The zip already contains the repo with all changes committed on a branch called `feature/devops-setup`.
```bash
# unzip CYPHER-devops.zip, then:
cd CYPHER
git push -u origin feature/devops-setup
git push origin main:develop          # creates the develop branch from main
```
On GitHub: open a PR `feature/devops-setup → develop`, merge it. 📸 PR page.
Then PR `develop → main`, merge. 📸 branches + commit history.

> Before merging, make sure `cypher/instance/app.db` does NOT appear in the repo (it's a local DB and is now in .gitignore).

## Day 1 (optional) — Docker locally (Task 2)
Only if your laptop has Docker Desktop and decent wifi. Otherwise do these exact commands on EC2 tomorrow (it counts the same — screenshot the terminal):
```bash
docker build -t cypher .
docker run -d --name cypher-local -p 5000:5000 -e APP_VERSION=local cypher
docker ps            # wait ~20s, STATUS shows (healthy)
curl localhost:5000/health
```
📸 build output, `docker ps`, app in browser.

---

## Day 2 — AWS + Jenkins (Tasks 3 & 4)

### 1. IAM role
IAM → Policies → Create policy → JSON → paste `deploy/aws/iam-policy.json` → name `cypher-ec2-policy`.
IAM → Roles → Create role → AWS service → **EC2** → attach `cypher-ec2-policy` → name `cypher-ec2-role`. 📸

### 2. ECR repository
ECR → Create repository → private → name `cypher` → enable *Scan on push*.
Open it → Lifecycle policy → paste `deploy/aws/ecr-lifecycle-policy.json` (JSON editor). 📸

### 3. EC2 instance
EC2 → Launch instance:
- Ubuntu Server 24.04, **t3.small** (t3.medium if you have credits; t2/t3.micro will crash)
- Key pair: create one, keep the .pem file safe (never commit it)
- Storage: 20 GB
- Security group: SSH 22 from **My IP**, HTTP 80 from anywhere, Custom TCP 8080 from anywhere
- Advanced details → IAM instance profile → `cypher-ec2-role`

📸 instance details + security group.

### 4. Install everything
```bash
ssh -i your-key.pem ubuntu@<EC2-PUBLIC-DNS>
git clone https://github.com/Devansh42-cyber/CYPHER.git
sudo bash CYPHER/deploy/setup-ec2.sh        # ~5 min
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

### 5. Jenkins first-time setup
Open `http://<EC2-PUBLIC-DNS>:8080` → paste the password → **Install suggested plugins** → create admin user.
- Manage Jenkins → Plugins → Available: install **Pipeline: Stage View** (and **GitHub** if not already there).
- Manage Jenkins → Credentials → System → Global → Add: kind **Secret text**, ID `aws-account-id`, secret = your 12-digit account ID. 📸 (value is hidden)

### 6. Pipeline job
New Item → `cypher-pipeline` → **Pipeline**:
- Build Triggers: ✅ **GitHub hook trigger for GITScm polling**
- Pipeline: *Pipeline script from SCM* → Git → `https://github.com/Devansh42-cyber/CYPHER.git` → branch `*/main` → script path `Jenkinsfile`
Save → **Build Now** once manually (first run registers the trigger).

### 7. GitHub webhook
Repo → Settings → Webhooks → Add:
- Payload URL: `http://<EC2-PUBLIC-DNS>:8080/github-webhook/` (trailing slash matters)
- Content type: `application/json`, event: *Just the push event*
📸 Recent deliveries showing a green tick.

### 8. Check
- Pipeline all green 📸 stage view + console
- ECR shows image tags 📸
- `http://<EC2-PUBLIC-DNS>` shows the app; footer shows the version
- `curl http://<EC2-PUBLIC-DNS>/health`
- Reboot test: `sudo reboot`, wait 2 min, app comes back by itself 📸 `docker ps`

---

## Day 3 — CloudFront (Task 5) + demo (Task 6)

### CloudFront distribution
CloudFront → Create distribution:
- Origin domain: paste the **EC2 public DNS** (`ec2-...compute.amazonaws.com`, not the IP)
- Protocol: **HTTP only**, port 80
- Viewer protocol policy: **Redirect HTTP to HTTPS**
- Allowed HTTP methods: **GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE**
- Cache policy: **CachingDisabled**; Origin request policy: **AllViewerExceptHostHeader**
- WAF: do not enable (costs money)
Create. Wait ~5–10 min until *Deployed*.

Then Behaviors → Create behavior:
- Path pattern `/static/*`, same origin, Redirect HTTP→HTTPS
- Cache policy: **UseOriginCacheControlHeaders-QueryStrings**
📸 behaviors list.

Copy the distribution ID (starts with `E...`) into `CLOUDFRONT_DISTRIBUTION_ID` in the `Jenkinsfile` (via feature branch → PR, which also gives you more PR history).

Open `https://dxxxx.cloudfront.net` → app works, scan a URL. 📸

### Demo (Task 6)
1. `git checkout develop && git pull && git checkout -b feature/ui-update`
2. Change something visible, e.g. the `<h1>`/title text in `cypher/templates/index.html` or a colour in `cypher/static/css/index.css`.
3. Commit, push, PR → develop → PR → main.
4. 📸 webhook delivery → Jenkins build running → all green → new tag in ECR → CloudFront page with the change and the new version number in the footer.

### Stop the bill
When you're done for the day: EC2 → Instance state → **Stop** (not terminate). Note: the public DNS changes when you stop/start, so update the CloudFront origin and webhook URL after restarting — or allocate an **Elastic IP** to keep it fixed (AWS charges a small hourly fee for public IPv4 addresses either way).

---

## If something breaks
| Symptom | Fix |
|---|---|
| `permission denied ... docker.sock` in Jenkins | `sudo systemctl restart jenkins` (group change needs a restart) |
| `no basic auth credentials` / ECR login fails | IAM role not attached to the instance, or wrong region |
| Webhook shows red ✗ | Port 8080 not open, or missing trailing `/` in URL |
| Build killed / Jenkins very slow | Instance too small; check `free -h`, use t3.small+ |
| CloudFront 502/504 | Origin must be the EC2 DNS, HTTP only, port 80; check app on `http://<EC2-DNS>` first |
| `POST` gives 403 on CloudFront | Allowed methods must include POST |
