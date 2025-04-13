#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}======= News & Content Downloader GitHub Upload Helper =======${NC}"
echo -e "This script will help you upload your project to GitHub\n"

# Create .gitignore file
echo -e "${GREEN}Creating .gitignore file...${NC}"
cat > ../.gitignore << EOL
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environments
venv/
ENV/
env/

# IDE files
.idea/
.vscode/
*.swp
*.swo

# OS specific files
.DS_Store
Thumbs.db

# Application specific
credentials.json
*.log
EOL

# Make sure directories exist
echo -e "${GREEN}Creating required directories...${NC}"
mkdir -p sources
mkdir -p downloads
touch downloads/.gitkeep

# Initialize git if needed
echo -e "${GREEN}Initializing Git repository...${NC}"
cd ..
if [ ! -d .git ]; then
    git init
fi

# Configure git if needed
if [ -z "$(git config --get user.name)" ]; then
    echo -e "${YELLOW}Git user.name not set. Please enter your name:${NC}"
    read name
    git config --global user.name "$name"
fi

if [ -z "$(git config --get user.email)" ]; then
    echo -e "${YELLOW}Git user.email not set. Please enter your email:${NC}"
    read email
    git config --global user.email "$email"
fi

# Check if remote repository is configured
REMOTE_URL=$(git remote get-url origin 2>/dev/null)
if [ -z "$REMOTE_URL" ]; then
    echo -e "${YELLOW}No remote repository configured.${NC}"
    echo -e "${YELLOW}Please create a new repository on GitHub first.${NC}"
    echo -e "${YELLOW}Enter your GitHub repository URL (e.g., https://github.com/username/repo.git):${NC}"
    read repo_url
    
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo -e "${GREEN}Remote repository configured: $repo_url${NC}"
    else
        echo -e "${RED}No repository URL provided. Exiting.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}Remote repository already configured: $REMOTE_URL${NC}"
fi

# Add all files
echo -e "${GREEN}Adding files to Git...${NC}"
git add -A

# Commit changes
echo -e "${YELLOW}Enter a commit message (e.g., 'Initial commit' or 'Update application files'):${NC}"
read commit_message

if [ -z "$commit_message" ]; then
    commit_message="Update News & Content Downloader files"
fi

git commit -m "$commit_message"

# Push to GitHub
echo -e "${GREEN}Pushing to GitHub...${NC}"
git push -u origin master || git push -u origin main

echo -e "\n${BLUE}✅ Done! Your News & Content Downloader is now on GitHub.${NC}"
echo -e "${BLUE}You can view it at: ${REMOTE_URL}${NC}" 