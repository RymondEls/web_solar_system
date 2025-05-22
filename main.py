import json
import asyncio
import logging
import time
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import numpy as np
from typing import List, Optional
from utils.json_load import load_bodies_from_json, save_bodies_to_json
from operations.orbit_simulation import simulate_orbits
from utils.scene_interaction import SceneInteraction
from entities.spacecraft import Spacecraft

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

try:
    bodies = load_bodies_from_json("config/solar_system.json")
    logger.info(f"Loaded {len(bodies)} bodies from solar_system.json")
    logger.info(f"Bodies: {[body.name for body in bodies]}")
    sun = next((body for body in bodies if body.name.lower() == "sun"), None)
    if sun:
        logger.info(f"Sun position: {sun.position.tolist()}")
    else:
        logger.warning("Sun not found in bodies")
except Exception as e:
    logger.error(f"Failed to load solar_system.json: {e}")
    bodies = []

sun_position = sun.position if sun else np.array([0, 0], dtype=float)
scene = SceneInteraction(
    scale=250 / 1.496e11,
    offset=np.array([960, 480], dtype=float) - sun_position * (250 / 1.496e11),
    tracked_body="Sun" if sun else None,
    dragging=False,
    last_mouse_pos=(0, 0),
    pause=False,
    time_scale=1
)
dt = 3600

class BodyData(BaseModel):
    name: str
    type: str
    mass: float
    position: List[float]
    velocity: List[float]
    color: List[int]
    radius: float
    temperature: Optional[float] = None
    atmosphere: Optional[str] = None
    surface: Optional[str] = None
    parent_planet: Optional[str] = None
    tail_length: Optional[float] = None
    composition: Optional[str] = None
    mission: Optional[str] = None

class SceneData(BaseModel):
    scale: float
    offset: List[float]
    pause: bool
    time_scale: float
    tracked_body: Optional[str] = None

class SpacecraftLaunch(BaseModel):
    name: str
    mass: float
    position: List[float]
    velocity: List[float]
    radius: float
    mission: str

class PanData(BaseModel):
    dx: float
    dy: float

def bodies_to_dict(bodies):
    return [{
        "name": body.name,
        "type": body.type,
        "position": body.position.tolist(),
        "velocity": body.velocity.tolist(),
        "color": body.color,
        "radius": body.radius,
        "tail_length": getattr(body, 'tail_length', None)
    } for body in bodies]

@app.websocket("/ws/simulation")
async def simulation_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            start_time = time.time()
            if not scene.pause:
                effective_time_scale = min(scene.time_scale, 50)
                simulate_orbits(bodies, dt, effective_time_scale)
                for body in bodies:
                    if hasattr(body, 'trajectory'):
                        body.trajectory.append(body.position.copy())
                        if len(body.trajectory) > 100:
                            body.trajectory.pop(0)
            if scene.tracked_body:
                tracked_found = False
                logger.debug(f"Available bodies: {[body.name for body in bodies]}")
                for body in bodies:
                    if body.name == scene.tracked_body:
                        scene.offset[0] = 960 - body.position[0] * scene.scale
                        scene.offset[1] = 480 - body.position[1] * scene.scale
                        logger.debug(f"Tracking {scene.tracked_body}, offset: {scene.offset.tolist()}")
                        tracked_found = True
                        break
                if not tracked_found:
                    logger.warning(f"Tracked body {scene.tracked_body} not found")
                    scene.tracked_body = None
            await websocket.send_json({
                "bodies": bodies_to_dict(bodies),
                "scene": {
                    "scale": scene.scale,
                    "offset": scene.offset.tolist(),
                    "pause": scene.pause,
                    "time_scale": scene.time_scale,
                    "tracked_body": scene.tracked_body
                }
            })
            elapsed = time.time() - start_time
            logger.debug(f"Simulation step took {elapsed:.3f}s")
            await asyncio.sleep(0.05)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        logger.error("index.html not found in static/")
        raise HTTPException(status_code=404, detail="index.html not found")
    except Exception as e:
        logger.error(f"Error reading index.html: {e}")
        raise HTTPException(status_code=500, detail="Error reading index.html")

@app.get("/bodies", response_model=List[BodyData])
async def get_bodies():
    logger.info(f"Returning {len(bodies)} bodies")
    return [body.to_dict() for body in bodies]

@app.get("/scene", response_model=SceneData)
async def get_scene():
    return {
        "scale": scene.scale,
        "offset": scene.offset.tolist(),
        "pause": scene.pause,
        "time_scale": scene.time_scale,
        "tracked_body": scene.tracked_body
    }

@app.post("/scene/pause")
async def toggle_pause():
    scene.pause = not scene.pause
    logger.info(f"Pause toggled to {scene.pause}")
    return {"pause": scene.pause}

@app.post("/scene/time_scale/{factor}")
async def adjust_time_scale(factor: float):
    scene.time_scale = max(0.1, min(scene.time_scale * factor, 50))
    logger.info(f"Time scale adjusted to {scene.time_scale}")
    return {"time_scale": scene.time_scale}

@app.post("/scene/zoom/{factor}")
async def zoom(factor: float):
    scene.scale *= factor
    logger.info(f"Zoom adjusted to scale {scene.scale}")
    return {"scale": scene.scale}

@app.post("/scene/pan")
async def pan(data: PanData):
    logger.info(f"Pan requested: dx={data.dx}, dy={data.dy}")
    if data.dx is None or data.dy is None:
        logger.error("Invalid dx or dy values")
        raise HTTPException(status_code=422, detail="dx and dy must be numbers")
    scene.offset[0] += data.dx
    scene.offset[1] += data.dy
    logger.debug(f"New offset: {scene.offset.tolist()}")
    return {"offset": scene.offset.tolist()}

@app.post("/scene/track/{body_name}")
async def track_body(body_name: str):
    logger.info(f"Requested tracking for body: {body_name}")
    for body in bodies:
        if body.name == body_name:
            scene.tracked_body = body_name
            logger.info(f"Tracking set to {body_name}")
            return {"tracked_body": scene.tracked_body}
    logger.error(f"Body {body_name} not found")
    raise HTTPException(status_code=404, detail="Body not found")

@app.post("/scene/untrack")
async def untrack_body():
    scene.tracked_body = None
    logger.info("Tracking disabled")
    return {"tracked_body": None}

@app.post("/spacecraft/launch", response_model=BodyData)
async def launch_spacecraft(data: SpacecraftLaunch):
    spacecraft = Spacecraft(
        name=data.name,
        type="spacecraft",
        mass=data.mass,
        position=data.position,
        velocity=data.velocity,
        color=[255, 255, 255],
        radius=data.radius,
        mission=data.mission
    )
    bodies.append(spacecraft)
    logger.info(f"Launched spacecraft: {data.name}")
    return spacecraft.to_dict()

@app.get("/study/atmosphere/{body_name}")
async def study_atmosphere(body_name: str):
    for body in bodies:
        if body.name == body_name and body.type == "planet":
            if hasattr(body, 'atmosphere'):
                return {"result": f"Изучение атмосферы {body.name}: {body.atmosphere}"}
            return {"result": f"У {body.name} нет атмосферы."}
    raise HTTPException(status_code=404, detail="Planet not found")

@app.get("/study/surface/{body_name}")
async def study_surface(body_name: str):
    for body in bodies:
        if body.name == body_name and body.type == "planet":
            if hasattr(body, 'surface'):
                return {"result": f"Изучение поверхности {body.name}: {body.surface}"}
            return {"result": f"Данные о поверхности {body.name} отсутствуют."}
    raise HTTPException(status_code=404, detail="Planet not found")

@app.get("/collect/data/{body_name}")
async def collect_data(body_name: str):
    for body in bodies:
        if body.name == body_name:
            result = {
                "name": body.name,
                "mass": body.mass,
                "position": body.position.tolist(),
                "velocity": body.velocity.tolist(),
                "type": body.type
            }
            if hasattr(body, 'atmosphere'):
                result["atmosphere"] = body.atmosphere
            if hasattr(body, 'surface'):
                result["surface"] = body.surface
            if hasattr(body, 'temperature'):
                result["temperature"] = body.temperature
            if hasattr(body, 'parent_planet'):
                result["parent_planet"] = body.parent_planet
            if hasattr(body, 'tail_length'):
                result["tail_length"] = body.tail_length
            if hasattr(body, 'composition'):
                result["composition"] = body.composition
            if hasattr(body, 'mission'):
                result["mission"] = body.mission
            return result
    raise HTTPException(status_code=404, detail="Body not found")

@app.get("/trajectory/{body_name}")
async def get_trajectory(body_name: str):
    for body in bodies:
        if body.name == body_name:
            return {"trajectory": [pos.tolist() for pos in body.trajectory]}
    raise HTTPException(status_code=404, detail="Body not found")

@app.post("/save")
async def save_state():
    save_bodies_to_json("config/solar_system_state.json", bodies)
    return {"message": "State saved successfully"}
