@echo off
echo ================================
echo  Java Streams Mastery - Server
echo ================================
echo.
echo Starting server on http://127.0.0.1:3000
echo Opening browser...
echo.
start "" http://127.0.0.1:3000/java-streams-mastery.html
python -m http.server 3000 --bind 127.0.0.1
pause
