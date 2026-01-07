# Web Test Agent - AI-Powered Testing Platform

An intelligent web testing platform powered by LangGraph and OpenAI, designed to automate web testing through natural language instructions.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python run.py

# 3. Open browser
http://localhost:5000
```

## ✨ Features

- 🤖 **AI-Powered Agent**: LangGraph-based intelligent test automation
- ⚡ **Fast & Efficient**: Quick test execution with real-time feedback
- 📱 **Responsive Design**: Clean, modern UI that works on all devices
- 🔒 **Secure**: Environment-based API key management
- 📊 **Multi-Page Platform**: Complete website with navigation

## 📄 Pages

| Page | Route | Description |
|------|-------|-------------|
| **Home** | `/` | Platform overview and features |
| **Test Console** | `/test` | Interactive testing interface with AI agent |
| **Documentation** | `/docs` | API documentation and guides |
| **About** | `/about` | Project information and technology stack |

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **LangGraph** - Agent orchestration
- **OpenAI API** - Language processing
- **python-dotenv** - Environment management

### Frontend
- **HTML5** - Structure
- **CSS3** - Clean, modern styling
- **Vanilla JavaScript** - Interactivity
- **Inter Font** - Professional typography

## 📁 Project Structure

```
Website - testing AI Agent/
├── app.py                 # Flask application with routes
├── agent.py              # LangGraph agent implementation
├── run.py                # Application runner
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (API keys)
├── templates/            # HTML templates
│   ├── index.html       # Home page
│   ├── test.html        # Test console
│   ├── docs.html        # Documentation
│   └── about.html       # About page
└── static/              # Static assets
    └── style.css        # Global styles
```

## 🔌 API Endpoints

### POST /api/agent
Send instructions to the LangGraph agent.

**Request**:
```json
{
  "input": "Your test instruction"
}
```

**Response**:
```json
{
  "status": "success",
  "message": "Agent response",
  "input": "Original input"
}
```

### GET /health
Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "service": "Web Test Agent - Milestone 1"
}
```

## 💡 Usage

1. Navigate to the **Test Console** page (`/test`)
2. Use the interactive test elements:
   - Click buttons to test interactions
   - Fill out and submit forms
   - Navigate between sections
3. Send natural language instructions to the AI agent
4. View real-time responses and results

## 🎨 Design Philosophy

This platform follows a **clean and minimal design approach**:
- ✓ Only essential elements displayed
- ✓ Clear navigation between pages
- ✓ Professional color scheme (blue primary, clean grays)
- ✓ Consistent spacing and typography
- ✓ Focus on functionality and usability

## ⚙️ Environment Variables

Create a `.env` file with:

```env
OPENAI_API_KEY=your_api_key_here
PORT=5000
DEBUG=True
```

## 🔍 Verification

To verify the setup is working:

1. ✅ **Dependencies Installed**: `pip list` shows Flask, LangGraph, etc.
2. ✅ **Server Running**: Access `http://localhost:5000`
3. ✅ **Pages Load**: Navigate between Home, Test, Docs, About
4. ✅ **Test Elements Work**: Click buttons, submit forms
5. ✅ **Agent Responds**: Send message to AI agent and receive response
6. ✅ **Health Check**: `http://localhost:5000/health` returns JSON

## 📝 Milestone Information

**Current**: Milestone 1 ✓
- ✓ Multi-page website structure
- ✓ Clean, professional UI design
- ✓ LangGraph agent integration
- ✓ Interactive test elements
- ✓ API endpoint for agent communication
- ✓ Complete documentation

## 🚦 Next Steps (Future Milestones)

- [ ] Enhanced LLM integration
- [ ] Advanced test automation
- [ ] Test result storage
- [ ] User authentication
- [ ] Comprehensive reporting

## 📞 Support

For questions or support:
- Visit the **Documentation** page (`/docs`)
- Use the **Test Console** to interact with the AI agent
- Check the **About** page for project details

---

**Built with ❤️ using Flask, LangGraph, and OpenAI**
