#!/usr/bin/env python3
import argparse
import csv
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

WINDOW_SIZES = [1, 2, 5, 10, 20, 50]
FIXED_RATE_PERCENT = 10


def write_csv(path: Path, rows: List[dict], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def mean(xs: List[float]) -> float:
    return sum(xs) / len(xs)


def _kill_proc(p: Optional[subprocess.Popen]) -> None:
    if p is None:
        return
    try:
        if p.poll() is None:
            p.kill()
    except Exception:
        pass
    try:
        p.wait(timeout=1.0)
    except Exception:
        pass


def files_match(path1: str, path2: str) -> bool:
    with open(path1, "rb") as f1, open(path2, "rb") as f2:
        while True:
            b1 = f1.read(8192)
            b2 = f2.read(8192)
            if b1 != b2:
                return False
            if not b1:
                return True


def run_one_transfer(
    option: str,
    window_size: int,
    attempt_idx: int,
    file_path: str,
    sender_py: str,
    receiver_py: str,
    out_path: str,
    base_port: int,
    timeout_s: float,
    hard_timeout_s: float,
    recv_bind_wait_s: float,
) -> Tuple[Optional[float], str]:
    assert option in ("opt1", "opt2", "opt3", "opt4", "opt5")

    p = FIXED_RATE_PERCENT / 100.0
    port = base_port + (window_size * 100) + attempt_idx
    seed = (window_size * 1000) + attempt_idx

    devnull = subprocess.DEVNULL
    linger_s = 2.0 if option in ("opt2", "opt4") else 0.2

    recv_cmd = [
        sys.executable,
        receiver_py,
        "--port", str(port),
        "--out", out_path,
        "--seed", str(seed),
        "--linger", str(linger_s),
        "--quiet",
    ]

    if option == "opt3":
        recv_cmd += ["--data-biterr", str(p)]
    elif option == "opt5":
        recv_cmd += ["--data-loss", str(p)]

    send_cmd = [
        sys.executable,
        sender_py,
        "--host", "127.0.0.1",
        "--port", str(port),
        "--file", file_path,
        "--window", str(window_size),
        "--timeout", str(timeout_s),
        "--seed", str(seed),
        "--quiet",
    ]

    if option == "opt2":
        send_cmd += ["--ack-biterr", str(p)]
    elif option == "opt4":
        send_cmd += ["--ack-loss", str(p)]

    recv_p: Optional[subprocess.Popen] = None
    send_p: Optional[subprocess.Popen] = None

    try:
        recv_p = subprocess.Popen(recv_cmd, stdout=devnull, stderr=devnull)
        time.sleep(recv_bind_wait_s)

        t0 = time.perf_counter()
        send_p = subprocess.Popen(send_cmd, stdout=devnull, stderr=devnull)

        try:
            send_rc = send_p.wait(timeout=hard_timeout_s)
        except subprocess.TimeoutExpired:
            _kill_proc(send_p)
            _kill_proc(recv_p)
            return None, "TIMEOUT"

        t1 = time.perf_counter()

        if send_rc != 0:
            _kill_proc(recv_p)
            return None, "SENDER_FAIL"

        try:
            recv_rc = recv_p.wait(timeout=hard_timeout_s)
        except subprocess.TimeoutExpired:
            _kill_proc(recv_p)
            return None, "RECEIVER_TIMEOUT"

        if recv_rc != 0:
            return None, "RECEIVER_FAIL"

        if not Path(out_path).exists():
            return None, "RECEIVER_FAIL"

        if not files_match(file_path, out_path):
            return None, "FILE_MISMATCH"

        return (t1 - t0), "OK"

    finally:
        if send_p is not None and send_p.poll() is None:
            _kill_proc(send_p)
        if recv_p is not None and recv_p.poll() is None:
            _kill_proc(recv_p)


def gnuplot_available() -> bool:
    return shutil.which("gnuplot") is not None


def write_gnuplot_script(results_dir: Path, avg_csv: Path, plot_png: Path) -> Path:
    gp_path = results_dir / "phase4_chart2.gp"
    gp = f"""\
set terminal pngcairo size 1400,800
set output "{plot_png.as_posix()}"
set title "Phase 4: Completion Time vs Window Size (10% Loss/Error)"
set xlabel "window size"
set ylabel "completion time (seconds)"
set grid
set key left top
set datafile separator ","
plot "{avg_csv.as_posix()}" using 1:2 with linespoints title "Option 1 (No loss/errors)", \\
     "{avg_csv.as_posix()}" using 1:4 with linespoints title "Option 2 (ACK bit-errors)", \\
     "{avg_csv.as_posix()}" using 1:6 with linespoints title "Option 3 (DATA bit-errors)", \\
     "{avg_csv.as_posix()}" using 1:8 with linespoints title "Option 4 (ACK loss)", \\
     "{avg_csv.as_posix()}" using 1:10 with linespoints title "Option 5 (DATA loss)"
"""
    gp_path.write_text(gp)
    return gp_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--max-attempts", type=int, default=20)
    ap.add_argument("--timeout", type=float, default=0.2)
    ap.add_argument("--hard-timeout", type=float, default=60.0)
    ap.add_argument("--base-port", type=int, default=12000)
    ap.add_argument("--sender", default="src/sender.py")
    ap.add_argument("--receiver", default="src/receiver.py")
    ap.add_argument("--results-dir", default="results")
    ap.add_argument("--recv-bind-wait", type=float, default=0.05)
    ap.add_argument("--plot", action="store_true")
    args = ap.parse_args()

    if args.max_attempts < args.runs:
        raise SystemExit("--max-attempts must be >= --runs")

    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    raw_csv = results_dir / "phase4_chart2_raw.csv"
    avg_csv = results_dir / "phase4_chart2_avg.csv"
    plot_png = results_dir / "phase4_chart2.png"

    raw_rows: List[dict] = []
    option_names = ("opt1", "opt2", "opt3", "opt4", "opt5")

    times_ok: Dict[str, List[List[float]]] = {
        opt: [[] for _ in range(len(WINDOW_SIZES))]
        for opt in option_names
    }

    for opt in option_names:
        for w_i, window_size in enumerate(WINDOW_SIZES):
            ok_count = 0
            attempt = 0

            while ok_count < args.runs and attempt < args.max_attempts:
                out_path = str(results_dir / f"tmp_chart2_{opt}_w{window_size}_ok{ok_count}_att{attempt}.bin")

                dt, status = run_one_transfer(
                    option=opt,
                    window_size=window_size,
                    attempt_idx=attempt,
                    file_path=args.file,
                    sender_py=args.sender,
                    receiver_py=args.receiver,
                    out_path=out_path,
                    base_port=args.base_port,
                    timeout_s=args.timeout,
                    hard_timeout_s=args.hard_timeout,
                    recv_bind_wait_s=args.recv_bind_wait,
                )

                raw_rows.append(
                    {
                        "option": opt,
                        "window_size": window_size,
                        "run": ok_count,
                        "attempt": attempt,
                        "status": status,
                        "seconds": f"{dt:.6f}" if (status == "OK" and dt is not None) else "",
                    }
                )

                if status == "OK" and dt is not None:
                    times_ok[opt][w_i].append(dt)
                    ok_count += 1
                else:
                    print(f"{opt} window={window_size:>2} attempt={attempt} -> {status}", flush=True)

                attempt += 1

            ok_list = times_ok[opt][w_i]
            if ok_list:
                avg = mean(ok_list)
                print(f"{opt} window={window_size:>2} done ok={len(ok_list)}/{args.runs} attempts={attempt} avg={avg:.3f}s", flush=True)
            else:
                print(f"{opt} window={window_size:>2} done ok=0/{args.runs} attempts={attempt} avg=NA", flush=True)

            if ok_count < args.runs:
                print(
                    f"WARNING: {opt} window={window_size} only got {ok_count}/{args.runs} OK runs after {attempt} attempts.",
                    flush=True,
                )

    write_csv(raw_csv, raw_rows, fieldnames=["option", "window_size", "run", "attempt", "status", "seconds"])

    avg_rows: List[dict] = []
    for w_i, window_size in enumerate(WINDOW_SIZES):
        row = {"window_size": window_size}
        for opt in option_names:
            ok_list = times_ok[opt][w_i]
            row[f"{opt}_avg"] = f"{mean(ok_list):.6f}" if ok_list else ""
            row[f"{opt}_ok_runs"] = len(ok_list)
        avg_rows.append(row)

    write_csv(
        avg_csv,
        avg_rows,
        fieldnames=[
            "window_size",
            "opt1_avg", "opt1_ok_runs",
            "opt2_avg", "opt2_ok_runs",
            "opt3_avg", "opt3_ok_runs",
            "opt4_avg", "opt4_ok_runs",
            "opt5_avg", "opt5_ok_runs",
        ],
    )

    gp_path = write_gnuplot_script(results_dir, avg_csv, plot_png)

    if args.plot:
        if gnuplot_available():
            subprocess.run(["gnuplot", gp_path.as_posix()], check=False)
            if plot_png.exists():
                print(f"\nPlot created: {plot_png}", flush=True)
            else:
                print("\nTried to plot with gnuplot, but PNG was not created.", flush=True)
        else:
            print("\n--plot requested but gnuplot not found. CSV + .gp script still generated.", flush=True)

    print(f"\nWrote:\n  {raw_csv}\n  {avg_csv}\n  {gp_path}" + (f"\n  {plot_png}" if plot_png.exists() else ""), flush=True)


if __name__ == "__main__":
    main()