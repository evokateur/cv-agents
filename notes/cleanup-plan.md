# Repository Cleanup Plan

## Objective

Make the repository presentable for public viewing while keeping professional CV information visible and removing only truly sensitive content.

## Step-by-Step Cleanup Plan

### 1. **Backup First**

```bash
git checkout -b cleanup-prep
git checkout -b private-backup  # Keep original intact
git checkout cleanup-prep
```

### 2. **Remove Sensitive Content**

```bash
rm notes/automattic/application-questions.md  # Contains API secret
rm -rf notes/lets-eat-grandma/  # Internal service communication
rm -rf lets-eat-grandma/drafts/  # Work-in-progress documents
rm cv.aux cv.log cv.out  # LaTeX build artifacts
```

### 3. **Reorganize Structure**

```bash
mkdir reference/
mv notes/multiemployer*.md notes/work-exp-gpt.md reference/
mv notes/upwork-profile.md notes/web-master.md reference/
mkdir examples/submissions/
mv submissions/ examples/submissions/
```

### 4. **Add .gitignore**

```
*.aux
*.log
*.out
*.fdb_latexmk
*.fls
*.synctex.gz
__pycache__/
*.pyc
.DS_Store
```

### 5. **Clean Up Root Directory**

- [ ] Keep: Core JSON files, Python scripts, Makefile, templates/, examples/
- [ ] Keep: lets-eat-grandma/final/ (professional outputs)
- [ ] Organize: Move remaining notes/ content to reference/ or delete if not useful

### 6. **Update README.md**

Add sections explaining:

- [ ] What the repo does (CV generation system)
- [ ] How to use the templates
- [ ] Your contact info (since it's meant to be public)

## Content Categories

### **Content to REMOVE (Actually Sensitive)**

- [ ] `notes/automattic/application-questions.md` - Contains API secret token
- [ ] `notes/lets-eat-grandma/` - Internal service communication and drafts
- [ ] `lets-eat-grandma/drafts/` - Work-in-progress documents not ready for public view
- [ ] LaTeX build artifacts: `cv.aux`, `cv.log`, `cv.out`

### **Content to KEEP (Professional & Useful)**

- [ ] Your final CV data (`cv.json`, `backend-dev-cv.json`, `library-cv.json`) - Shows your experience
- [ ] Generated PDFs - Demonstrates the output
- [ ] Core templating system - Shows your technical skills
- [ ] `lets-eat-grandma/final/` - Polished, professional documents

### **Content to ORGANIZE Better**

- [ ] Move personal notes about work experience (`notes/multiemployer.md`, `notes/work-exp-gpt.md`) to a `reference/` folder
- [ ] Keep `submissions/la-clinica/` as an example of customization
- [ ] Clean up root directory by organizing loose files

## Result

A portfolio-like repository that showcases both your CV content and your technical ability to build automated document generation systems, with only truly sensitive content removed.

