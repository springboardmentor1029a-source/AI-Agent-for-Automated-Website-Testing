# AI-Agent-for-Automated-Website-Testing

## Directory Structure

```bash
(.venv) youvalkumar@Youvals-MacBook-Air youval-autoqa % tree -I 'node_modules'

├── backend
│   ├── ai_test_automation.py
│   ├── artifacts
│   │   └── groq_raw_20251227192237.txt
│   ├── data
│   │   ├── approved_scenario.json
│   │   ├── latest_analysis.json
│   │   ├── report_index.json
│   │   └── runs.json
│   ├── reports
│   │   └── run_20251227192244_faf2e5.pdf
│   ├── requirements.txt
│   └── screenshots
│       ├── run_20251226173024_9b0ef9.png
└── frontend
    ├── README.md
    ├── eslint.config.js
    ├── image.md
    ├── index.html
    ├── package-lock.json
    ├── package.json
    ├── src
    │   ├── App.jsx
    │   ├── assets
    │   │   ├── AI.png
    │   │   ├── AI_Analysis.png
    │   │   ├── Approval.png
    │   │   ├── Logo.png
    │   │   ├── Report-preview.png
    │   │   ├── Rpt.png
    │   │   ├── ai-agent-avatar.png
    │   │   ├── blue-space.avif
    │   │   ├── blue.png
    │   │   ├── hero-bg.jpg
    │   │   ├── icons
    │   │   │   ├── Action.png
    │   │   │   ├── Analyze.png
    │   │   │   ├── Beta_Testing.png
    │   │   │   ├── Bug.png
    │   │   │   ├── Checklist.png
    │   │   │   ├── Clock.png
    │   │   │   ├── Code.png
    │   │   │   ├── Defect.png
    │   │   │   ├── Deployment.png
    │   │   │   ├── Env.png
    │   │   │   ├── Fail.png
    │   │   │   ├── Goal.png
    │   │   │   ├── Implementation.png
    │   │   │   ├── Integration_Testing.png
    │   │   │   ├── Interface_Testing.png
    │   │   │   ├── Load_Testing.png
    │   │   │   ├── Navigation_Flow.png
    │   │   │   ├── Pass.png
    │   │   │   ├── Performance_Testing.png
    │   │   │   ├── Play.png
    │   │   │   ├── Process.png
    │   │   │   ├── Quality.png
    │   │   │   ├── Requirements.png
    │   │   │   ├── Risk.png
    │   │   │   ├── SOFTWARE.png
    │   │   │   ├── Security_Testing.png
    │   │   │   ├── Setting.png
    │   │   │   ├── Sprint.png
    │   │   │   ├── Stress_Testing.png
    │   │   │   ├── System_Testing.png
    │   │   │   ├── Target.png
    │   │   │   ├── Test_Plan.png
    │   │   │   ├── Testing.png
    │   │   │   ├── Unit_Testing.png
    │   │   │   ├── Upload.png
    │   │   │   └── Usability.png
    │   │   ├── main.png
    │   │   ├── marvel.avif
    │   │   ├── steps-flow.png
    │   │   ├── upload-illustration.png
    │   │   ├── waave.avif
    │   │   └── web_spiral.avif
    │   ├── components
    │   │   ├── BenefitCard.jsx
    │   │   ├── Common
    │   │   │   ├── ErrorBanner.jsx
    │   │   │   ├── FileDropzone.jsx
    │   │   │   ├── Loader.jsx
    │   │   │   ├── MetricCard.jsx
    │   │   │   ├── StatusBadge.jsx
    │   │   │   ├── StepTimeline.jsx
    │   │   │   └── TagPill.jsx
    │   │   ├── FeatureCard.jsx
    │   │   ├── Navbar.jsx
    │   │   ├── Sidebar.jsx
    │   │   └── TestimonialCard.jsx
    │   ├── context
    │   │   └── ThemeContext.jsx
    │   ├── index.css
    │   ├── main.jsx
    │   ├── pages
    │   │   ├── About.jsx
    │   │   ├── AnalysisReview.jsx
    │   │   ├── CapabilityPages.jsx
    │   │   ├── Contact.jsx
    │   │   ├── DataInput.jsx
    │   │   ├── ExecutionDashboard.jsx
    │   │   ├── Home.jsx
    │   │   ├── HowItWorks.jsx
    │   │   ├── RegressionCenter.jsx
    │   │   ├── Reports.jsx
    │   │   ├── Settings.jsx
    │   │   └── TestConsole.jsx
    │   ├── services
    │   │   ├── analysisService.js
    │   │   ├── api.js
    │   │   └── executionReportService.js
    │   └── styles
    │       ├── About.css
    │       ├── AnalysisReview.css
    │       ├── CapabilityPages.css
    │       ├── Contact.css
    │       ├── DataInput.css
    │       ├── ExecutionDashboard.css
    │       ├── Home.css
    │       ├── HowItWorks.css
    │       ├── Navbar.css
    │       ├── RegressionCenter.css
    │       ├── ReportsPage.css
    │       ├── SettingsPage.css
    │       ├── TestConsolePage.css
    │       ├── index.css
    │       └── layout.css
    └── vite.config.js
