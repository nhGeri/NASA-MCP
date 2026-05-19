@echo off
echo ========================================================
echo LIBRECHAT (SciChat) Inditasa a NASA projekt tesztelesehez
echo ========================================================
echo.

echo [1/3] Regi MCP_dinamic leallitasa (hogy ne utkozzon a port)...
cd /d "C:\Users\nagyh\source\repos\MCP_dinamic"
docker compose down

echo.
echo [2/3] Uj SciChat (NASA) felepitese es inditasa...
cd /d "C:\Users\nagyh\source\repos\SciChat"
docker compose up -d --build

echo.
echo [3/3] Bongeszo megnyitasa...
timeout /t 5 >nul
start http://localhost:3080/

echo.
echo KESZ! A LibreChat elindult! Ezt az ablakot bezarhatod.
pause
