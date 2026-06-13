@echo off
title TARS System Launcher
echo ===================================================
echo          STARTING TARS AUTONOMOUS SYSTEM
echo ===================================================
echo.

:: 1. Start the Flask Dashboard Server in a new window
echo Starting Dashboard Server...
start "TARS Dashboard Server" cmd /k ".\.venv\Scripts\python.exe dashboard\server.py"

:: Give the server a couple of seconds to boot up before launching the browser
timeout /t 3 /nobreak > nul

:: 2. Launch the frontend in the default browser
echo Opening Dashboard Frontend...
start http://localhost:5000

:: 3. Start the PyGame Visual Simulation in a new window
echo Starting Visual Simulation...
start "TARS Visual Simulation" cmd /k ".\.venv\Scripts\python.exe simulation\visual_sim.py"

:: 4. Start the Central Orchestrator in a new window
echo Starting Central Orchestrator...
start "TARS Central Orchestrator" cmd /k ".\.venv\Scripts\python.exe main.py"

echo.
echo All systems successfully launched!
echo Note: If you want to stop the double-voice issue, simply close either the Orchestrator or Simulation window.
pause
