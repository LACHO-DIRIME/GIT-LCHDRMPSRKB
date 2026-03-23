"""IMV/tools/scalar_monitor.py — REACTIVE_DATAFLOW. TASK_3.6 [P2][I3]"""
import json, time, sqlite3
from pathlib import Path
DB_PATH = Path(__file__).parent.parent / "data" / "sovereign.db"
POLL_INTERVAL = 30

def get_current_scalar(db_path: str = str(DB_PATH)) -> dict:
    try:
        conn = sqlite3.connect(db_path)
        row = conn.execute(
            "SELECT scalar, tx_count, crystal_count FROM system_state "
            "ORDER BY id DESC LIMIT 1"
        ).fetchone()
        conn.close()
        if row: return {"scalar": round(row[0],4), "tx_count": row[1], "crystal_count": row[2]}
        return {"scalar": 0.0, "tx_count": 0, "crystal_count": 0}
    except Exception as e:
        return {"scalar": 0.0, "error": str(e)}

def write_scalar_json(output_path="scalar_live.json") -> dict:
    data = get_current_scalar()
    data.update({"timestamp": time.time(), "iso_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    with open(output_path, "w") as f: json.dump(data, f, indent=2)
    return data

if __name__ == "__main__":
    print("Scalar monitor — polling every 30s")
    while True:
        r = write_scalar_json()
        print(f"[{r['iso_time']}] S={r['scalar']} TX={r.get('tx_count',0)}")
        time.sleep(POLL_INTERVAL)
