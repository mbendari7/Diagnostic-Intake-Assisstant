# 🛠️ Diagnostic Intake Portal

An intelligent, automated hardware and software diagnostic triage system powered by Python, Flask, and the Google Gemini 2.5 API. 

This application bridges the gap between non-technical users and IT professionals by automatically harvesting local system telemetry and using AI to correlate that hard data against the user's described symptoms.

## 🚀 The Core Problem This Solves

**The standard tech support workflow is broken.** When users experience a system failure, they often rely on standard Google searches or basic AI chatbots. The issue is that standard AI only knows what the user tells it (e.g., *"My screen goes black when I play games"*). It lacks the actual hardware context to provide a real answer, resulting in generic advice like *"Update your drivers."*

**The Diagnostic Intake Portal solves this.** Instead of relying on the user to accurately describe their hardware, this portal executes a secure, local telemetry scan the moment they hit submit. It merges their vague complaint with hard, real-time data (CPU temperatures, memory exhaustion, failing disk sectors, and resource-hogging background processes). 

The result is a Level-3 Technician diagnostic report that identifies the *actual* root cause, saving IT professionals hours of manual intake interviewing.

### Real-World Applications
* **Managed IT Service Providers (MSPs):** A highly efficient pre-intake tool to automatically triage and route client tickets.
* **Repair Shops (e.g., Digital Fixers):** A client-facing kiosk app to run initial diagnostics while the customer is dropping off their machine.
* **Enterprise Helpdesks:** An internal self-service portal for employees to automatically resolve Tier-1 issues before escalating to human support.

## 💻 Tech Stack

* **Backend:** Python 3.x, Flask
* **Hardware Telemetry Agent:** `psutil`, `platform` (OS-level metric extraction)
* **Artificial Intelligence:** Google Generative AI SDK (`gemini-2.5-flash`)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API for asynchronous UI updates)
* **Security:** `python-dotenv` for secure credential management

## ✨ Features

* **One-Click Local Telemetry:** Silently harvests CPU core usage, available memory, disk partition health, and the top memory/CPU-consuming background processes.
* **Context-Aware AI Engine:** Prompts the Gemini 2.5 API to act as an IT Level-3 Technician, correlating user symptoms with the harvested JSON data.
* **Conversational Memory:** Users can ask follow-up questions within the app. The AI retains the memory of the initial hardware scan and diagnosis for the entire session.
* **Structured Triage Reports:** Outputs clean, professional HTML reports with prioritized, step-by-step repair plans and clickable documentation links.
* **Responsive UI:** Features a clean, dark-mode/light-mode native OS aesthetic inspired by GitHub's Primer design system.

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/diagnostic-triage-portal.git](https://github.com/YOUR_USERNAME/diagnostic-triage-portal.git)
cd diagnostic-triage-portal
