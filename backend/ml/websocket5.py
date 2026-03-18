# backend/ml/websocket_final.py
# (Clean, Stable, Original Logic + Gaze Restriction)

import serial
import serial.tools.list_ports
import time
import csv
import subprocess
import os
import threading
from datetime import datetime
import asyncio
import websockets
import json
from queue import Queue

# --- Computer Vision Imports ---
import cv2
import mediapipe as mp
import numpy as np
import base64

# --- Configuration ---
COM_PORT = 'COM3'  
BAUD_RATE = 115200
SAMPLE_RATE = 256
DURATION_MIN = 4

# WebSocket Ports
WEBSOCKET_HOST = 'localhost'
EEG_PORT = 8765       # EEG Data
VERDICT_PORT = 8766   # ML Verdicts
GAZE_PORT = 8767      # Gaze Video Stream

EEG_SEND_RATE = 10    # Send every 10th sample to frontend
MAX_SAMPLES_PER_FILE = SAMPLE_RATE * DURATION_MIN * 60

# File Paths
FILENAME_1 = 'eeg_recording_file_1.csv'
FILENAME_2 = 'eeg_recording_file_2.csv'
MODEL_TEST_SCRIPT = 'predict4.py'
RESULTS_LOG = 'classification_results_log.txt'

# --- Gaze Settings ---
# If gaze focus is below this % (e.g., 0.50 = 50%), the verdict is flagged
GAZE_THRESHOLD_PERCENT = 0.50 

# --- Globals ---
eeg_clients = set()
verdict_clients = set()
gaze_clients = set()

eeg_loop = None
verdict_loop = None
gaze_loop = None

latest_verdict = {
    'state': 'UNKNOWN',
    'confidence': 'N/A',
    'beta_activity': 'N/A',
    'gaze_adherence': 'N/A',
    'timestamp': None,
    'session': 0
}
latest_gaze = "STARTING"
eeg_sample_queue = Queue()

# MediaPipe Setup
mp_face_mesh = mp.solutions.face_mesh
gaze_stats_lock = threading.Lock()
current_session_gaze_stats = {'center_frames': 0, 'total_frames': 0}


# -------------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------------

def log_result(message):
    """Simple file logging without console spam"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(RESULTS_LOG, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def decode_frame(base64_str):
    try:
        if ',' in base64_str:
            header, data = base64_str.split(',', 1)
        else:
            data = base64_str
        decoded_data = base64.b64decode(data)
        np_arr = np.frombuffer(decoded_data, np.uint8)
        return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except:
        return None

def process_frame_for_gaze(frame):
    """Calculates gaze direction from video frame"""
    gaze_text = "No Face"
    try:
        with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5, 
            min_tracking_confidence=0.5) as face_mesh:
            
            frame.flags.writeable = False
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                
                # Eye landmarks
                left_pupil = face_landmarks.landmark[473]
                right_pupil = face_landmarks.landmark[468]
                left_iris = [face_landmarks.landmark[i] for i in range(474, 478)]
                right_iris = [face_landmarks.landmark[i] for i in range(469, 472)]
                
                # Calculate Gaze Ratio
                l_dx = (left_iris[2].x - left_iris[0].x)
                r_dx = (right_iris[2].x - right_iris[0].x)
                if l_dx == 0: l_dx = 0.0001
                if r_dx == 0: r_dx = 0.0001

                l_center = sum(l.x for l in left_iris) / len(left_iris)
                r_center = sum(l.x for l in right_iris) / len(right_iris)
                
                left_gaze = (left_pupil.x - l_center) / l_dx
                right_gaze = (right_pupil.x - r_center) / r_dx
                avg_gaze = (left_gaze + right_gaze) / 2

                if avg_gaze > 0.02: gaze_text = "Looking Right"
                elif avg_gaze < -0.02: gaze_text = "Looking Left"
                else: gaze_text = "Looking Center"
        
        # Update Session Stats
        with gaze_stats_lock:
            current_session_gaze_stats['total_frames'] += 1
            if gaze_text == "Looking Center":
                current_session_gaze_stats['center_frames'] += 1
            
        return gaze_text
    except:
        return "Error"

def parse_classification_result(output_text):
    """Parses the output from predict4.py"""
    try:
        if 'success' in output_text:
            res = json.loads(output_text.strip())
            return res.get('focus_state', 'UNKNOWN'), res.get('confidence', 'N/A'), res.get('beta_activity', 'N/A')
        
        # Fallback keyword search
        import re
        conf_match = re.search(r'confidence[:\s]+([0-9.]+%?)', output_text, re.IGNORECASE)
        beta_match = re.search(r'beta[:\s]+([0-9.]+%?)', output_text, re.IGNORECASE)
        c_val = conf_match.group(1) if conf_match else 'N/A'
        b_val = beta_match.group(1) if beta_match else 'N/A'

        if 'NOT FOCUSED' in output_text.upper(): return 'NOT FOCUSED', c_val, b_val
        if 'FOCUSED' in output_text.upper(): return 'FOCUSED', c_val, b_val
    except: pass
    return "ERROR", "N/A", "N/A"

def display_focus_notification(focus_state, confidence, beta_pct, filename, duration_min):
    """Simple text notification instead of popups"""
    print(f"\n--- SESSION VERDICT: {focus_state} ---")
    print(f"File: {filename}")
    print(f"Confidence: {confidence}")
    print(f"Beta Activity: {beta_pct}")
    print("--------------------------------------\n")

# -------------------------------------------------------------------
# WebSocket Handlers
# -------------------------------------------------------------------

async def handle_eeg_client(websocket):
    global eeg_clients
    eeg_clients.add(websocket)
    try:
        await websocket.send(json.dumps({'type': 'connection', 'status': 'connected', 'port_type': 'eeg_signal'}))
        async for message in websocket: pass
    except: pass
    finally: eeg_clients.discard(websocket)

async def broadcast_eeg_sample(val):
    if eeg_clients:
        msg = json.dumps({'type': 'eeg_sample', 'timestamp': datetime.now().isoformat(), 'value': val})
        for c in list(eeg_clients):
            try: await c.send(msg)
            except: pass

async def handle_verdict_client(websocket):
    global verdict_clients
    verdict_clients.add(websocket)
    try:
        # Send initial state and last known verdict immediately upon connection
        await websocket.send(json.dumps({'type': 'connection', 'status': 'connected', 'message': 'Connected to ML Verdict Stream'}))
        if latest_verdict['timestamp']:
             await websocket.send(json.dumps({
                'type': 'verdict',
                'timestamp': datetime.now().isoformat(),
                'focus_state': latest_verdict['state'],
                'confidence': latest_verdict['confidence'],
                'beta_activity': latest_verdict['beta_activity'],
                'gaze_adherence': latest_verdict.get('gaze_adherence', 'N/A'),
                'session': latest_verdict['session']
            }))
        async for message in websocket: pass
    except: pass
    finally: verdict_clients.discard(websocket)

async def broadcast_verdict(data):
    if verdict_clients:
        msg = json.dumps({'type': 'verdict', 'timestamp': datetime.now().isoformat(), **data})
        for c in list(verdict_clients):
            try: await c.send(msg)
            except: pass

async def handle_gaze_client(websocket):
    global gaze_clients, latest_gaze
    gaze_clients.add(websocket)
    loop = asyncio.get_event_loop()
    try:
        await websocket.send(json.dumps({'type': 'connection', 'status': 'connected'}))  
        async for message in websocket:
            try:
                data = json.loads(message)
                if data.get('type') == 'video_frame':
                    frame = decode_frame(data['data'])
                    if frame is None: continue
                    
                    gaze_status = await loop.run_in_executor(None, process_frame_for_gaze, frame)
                    
                    if gaze_status != latest_gaze:
                        latest_gaze = gaze_status
                        await websocket.send(json.dumps({'type': 'gaze_update', 'status': gaze_status}))
            except: pass
    except: pass
    finally: gaze_clients.discard(websocket)

# -------------------------------------------------------------------
# Server Starters (Using Runner Pattern to Fix Asyncio Errors)
# -------------------------------------------------------------------

def start_eeg_server(loop):
    asyncio.set_event_loop(loop)
    global eeg_loop
    eeg_loop = loop
    async def runner():
        print(f"✓ EEG Server running on ws://{WEBSOCKET_HOST}:{EEG_PORT}")
        async with websockets.serve(handle_eeg_client, WEBSOCKET_HOST, EEG_PORT):
            await asyncio.Future()
    loop.run_until_complete(runner())

def start_verdict_server(loop):
    asyncio.set_event_loop(loop)
    global verdict_loop
    verdict_loop = loop
    async def runner():
        print(f"✓ Verdict Server running on ws://{WEBSOCKET_HOST}:{VERDICT_PORT}")
        async with websockets.serve(handle_verdict_client, WEBSOCKET_HOST, VERDICT_PORT):
            await asyncio.Future()
    loop.run_until_complete(runner())

def start_gaze_server(loop):
    asyncio.set_event_loop(loop)
    global gaze_loop
    gaze_loop = loop
    async def runner():
        print(f"✓ Gaze Server running on ws://{WEBSOCKET_HOST}:{GAZE_PORT}")
        async with websockets.serve(handle_gaze_client, WEBSOCKET_HOST, GAZE_PORT, max_size=5_000_000):
            await asyncio.Future()
    loop.run_until_complete(runner())

# -------------------------------------------------------------------
# Threads
# -------------------------------------------------------------------

def continuous_eeg_sender():
    global eeg_sample_queue, eeg_loop
    cnt = 0
    while True:
        try:
            val = eeg_sample_queue.get(timeout=1)
            cnt += 1
            if cnt % EEG_SEND_RATE == 0 and eeg_clients and eeg_loop:
                asyncio.run_coroutine_threadsafe(broadcast_eeg_sample(float(val)), eeg_loop)
        except: continue

def send_eeg_sample_sync(value):
    try: eeg_sample_queue.put_nowait(value)
    except: pass

def send_verdict_sync(verdict_data):
    global latest_verdict
    latest_verdict = verdict_data
    try:
        if verdict_clients and verdict_loop:
            asyncio.run_coroutine_threadsafe(broadcast_verdict(verdict_data), verdict_loop)
    except: pass

def run_model_classification(filename, session_num, gaze_percentage):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        gaze_pct_str = f"{gaze_percentage*100:.1f}%"
        
        log_result(f"Analyzing Session #{session_num} | File: {filename} | Gaze: {gaze_pct_str}")
        
        if not os.path.exists(filename): return
        
        # Run ML Script
        result = subprocess.run(['python', MODEL_TEST_SCRIPT, filename], capture_output=True, text=True, timeout=120)
        output = result.stdout + "\n" + result.stderr
        
        # Parse Result
        focus_state, confidence, beta_pct = parse_classification_result(output)
        
        # ---------------------------------------------------------
        # Apply Gaze Restriction Logic
        # ---------------------------------------------------------
        final_verdict = focus_state
        if gaze_percentage < GAZE_THRESHOLD_PERCENT:
            if focus_state == "FOCUSED" or focus_state == "UNKNOWN":
                final_verdict = "NOT FOCUSED"
                confidence = "High (Gaze Override)"
                log_result("-> Verdict Overridden: Low visual attention detected.")

        display_focus_notification(final_verdict, confidence, beta_pct, filename, DURATION_MIN)
        log_result(f"-> FINAL VERDICT: {final_verdict} (Beta: {beta_pct}, Gaze: {gaze_pct_str})")

        # Send to Frontend
        verdict_data = {
            'focus_state': final_verdict,
            'confidence': confidence,
            'beta_activity': beta_pct,
            'gaze_adherence': gaze_pct_str,
            'analysis_timestamp': timestamp,
            'session': session_num
        }
        send_verdict_sync(verdict_data)

    except Exception as e:
        log_result(f"Error in classification: {e}")

def classify_file_async(filename, session_num, gaze_percentage):
    t = threading.Thread(target=run_model_classification, 
                         args=(filename, session_num, gaze_percentage), 
                         daemon=True)
    t.start()
    return t

# -------------------------------------------------------------------
# Main Execution
# -------------------------------------------------------------------

if __name__ == "__main__":
    ser = None
    try:
        print("\n🌐 Starting Hardware & AI Servers...")
        
        # Start WebSocket Servers in background threads
        threading.Thread(target=start_gaze_server, args=(asyncio.new_event_loop(),), daemon=True).start()
        threading.Thread(target=start_eeg_server, args=(asyncio.new_event_loop(),), daemon=True).start()
        threading.Thread(target=start_verdict_server, args=(asyncio.new_event_loop(),), daemon=True).start()
        threading.Thread(target=continuous_eeg_sender, daemon=True).start()
        
        time.sleep(2)
        print(f"\n🔌 Connecting to Serial Port: {COM_PORT}...")
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
        print("✓ Serial Connected.")
        
        print("\n" + "="*60)
        print("SYSTEM LIVE. Monitoring EEG + Gaze.")
        print(f"NOTE: Users must look at screen > {GAZE_THRESHOLD_PERCENT*100}% of time.")
        print("="*60 + "\n")
        
        current_file_index = 1
        session_number = 0
        
        while True:
            session_number += 1
            active_file = FILENAME_1 if current_file_index == 1 else FILENAME_2
            prev_file = FILENAME_2 if current_file_index == 1 else FILENAME_1
            
            # If previous session exists, analyze it
            if session_number > 1:
                gaze_ratio = 1.0
                with gaze_stats_lock:
                    if current_session_gaze_stats['total_frames'] > 0:
                        gaze_ratio = current_session_gaze_stats['center_frames'] / current_session_gaze_stats['total_frames']
                    # Reset stats
                    current_session_gaze_stats = {'center_frames': 0, 'total_frames': 0}

                # Start analysis thread
                classify_file_async(prev_file, session_number - 1, gaze_ratio)
            
            print(f"🔴 Recording Session #{session_number} to {active_file}...")
            
            # Recording Loop
            with open(active_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['channel1', 'channel2'])
                
                samples = 0
                while samples < MAX_SAMPLES_PER_FILE:
                    line = ser.readline()
                    if line:
                        try:
                            line_str = line.decode('utf-8').strip()
                            val = float(line_str)
                            writer.writerow([val, val])
                            samples += 1
                            
                            # Send to live graph
                            send_eeg_sample_sync(val)
                            
                            progress = (samples / MAX_SAMPLES_PER_FILE) * 100
                            print(f"Rec: {progress:.1f}%", end='\r')
                        except: continue
            
            # Switch file
            current_file_index = 2 if current_file_index == 1 else 1

    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
    finally:
        if ser: ser.close()