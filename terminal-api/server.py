import asyncio, json, os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from render import RenderAsync
from render.sandbox import SandboxExecOutput, SandboxExecExit

app = FastAPI(title='ZYVORA Bash Sandbox')
render = RenderAsync()

@app.get('/health')
async def health():
    return {'ok': True, 'service': 'zyvora-bash-sandbox'}

@app.get('/terminal')
async def terminal():
    return FileResponse('../terminal.html')

async def run_command(sandbox_id: str, command: str, websocket: WebSocket):
    # Guest-side timeout limits long-running commands. The Render Sandbox is disposable.
    safe = f"timeout -k 2 25 bash -lc {json.dumps(command)}"
    async for event in render.sandboxes.exec(sandbox_id, safe):
        if isinstance(event, SandboxExecOutput):
            await websocket.send_json({'type': 'out', 'data': event.data})
        elif isinstance(event, SandboxExecExit):
            if event.exit_code != 0:
                await websocket.send_json({'type': 'err', 'data': f'command exited with code {event.exit_code}'})

@app.websocket('/ws')
async def ws(websocket: WebSocket):
    await websocket.accept()
    sandbox = None
    try:
        sandbox = await render.sandboxes.create(
            timeout_seconds=900,
            network_policy='deny-all',
        )
        await render.sandboxes.wait_until_running(sandbox.id, timeout_seconds=60)
        await websocket.send_json({'type': 'status', 'data': 'online'})
        await run_command(sandbox.id, 'printf "ZYVORA Linux sandbox\\n"; pwd; uname -a', websocket)
        while True:
            raw = await websocket.receive_text()
            payload = json.loads(raw)
            command = str(payload.get('command', '')).strip()
            if not command:
                continue
            if len(command) > 2000:
                await websocket.send_json({'type': 'err', 'data': 'command too long'})
                continue
            if command in {'exit', 'logout'}:
                await websocket.send_json({'type': 'out', 'data': 'Session closed.'})
                break
            await run_command(sandbox.id, command, websocket)
    except WebSocketDisconnect:
        pass
    except Exception as exc:
        try:
            await websocket.send_json({'type': 'err', 'data': f'sandbox error: {type(exc).__name__}'})
        except Exception:
            pass
    finally:
        if sandbox:
            try:
                await asyncio.wait_for(render.sandboxes.terminate(sandbox.id), timeout=15)
            except Exception:
                pass
