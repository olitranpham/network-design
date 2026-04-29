#!/usr/bin/env python3
import argparse
import csv
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Optional, Tuple

RATES = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]


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
    rate_percent: int,
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

    p = rate_percent / 100.0
    port = base_port + (rate_percent * 100) + attempt_idx
    seed = (rate_percent * 1000) + attempt_idx

    devnull = subprocess.DEVNULL

    recv_cmd = [
        sys.executable,
        receiver_py,
        "--port", str(port),
        "--out", out_path,
        "--seed", str(seed),
        "--linger", "0.2",
        "--quiet",
        "--data-loss", str(p),
    ]

    send_cmd = [
        sys.executable,
        sender_py,
        "--host", "127.0.0.1",
        "--port", str(port),
        "--file", file_path,
        "--timeout", str(timeout_s),
        "--seed", str(seed),
        "--quiet",
    ]

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


def write_chart1_gnuplot(results_dir: Path, avg_csv: Path, plot_png: Path) -> Path:
    gp_path = results_dir / "phase5_chart1.gp"
    gp = f"""\
set terminal pngcairo size 1400,800
set output "{plot_png.as_posix()}"
set title "Phase 5: Completion Time Under Packet Loss"
set xlabel "intentional packet loss rate (%)"
set ylabel "average completion time (seconds)"
set grid
set key left top
set xtics rotate by 45
set datafile separator ","
plot "{avg_csv.as_posix()}" using 1:2 with linespoints title "Phase 5 TCP-like protocol"
"""
    gp_path.write_text(gp)
    return gp_path


def write_cwnd_gnuplot(results_dir: Path, cwnd_csv: Path, plot_png: Path) -> Path:
    gp_path = results_dir / "phase5_cwnd.gp"
    gp = f"""\
set terminal pngcairo size 1400,800
set output "{plot_png.as_posix()}"
set title "Phase 5: Congestion Window Evolution"
set xlabel "event number"
set ylabel "cwnd"
set grid
set key left top
set datafile separator ","
plot "{cwnd_csv.as_posix()}" using 0:5 with linespoints title "cwnd"
"""
    gp_path.write_text(gp)
    return gp_path


def write_phase_comparison(results_dir: Path, phase5_avg_0: float) -> Path:
    csv_path = results_dir / "phase5_phase_comparison.csv"

    rows = [
        {"phase": "Phase 1", "seconds": "0.053"},
        {"phase": "Phase 2", "seconds": "0.059"},
        {"phase": "Phase 3", "seconds": "1.725"},
        {"phase": "Phase 4", "seconds": "2.866"},
        {"phase": "Phase 5", "seconds": f"{phase5_avg_0:.6f}"},
    ]

    write_csv(csv_path, rows, ["phase", "seconds"])
    return csv_path


def write_phase_comparison_gnuplot(results_dir: Path, comparison_csv: Path, plot_png: Path) -> Path:
    gp_path = results_dir / "phase5_phase_comparison.gp"
    gp = f"""\
set terminal pngcairo size 1200,700
set output "{plot_png.as_posix()}"
set title "Phase Comparison Using Same Transfer File"
set xlabel "phase"
set ylabel "completion time (seconds)"
set grid
set datafile separator ","
set style data histograms
set style fill solid
set boxwidth 0.6
set xtics rotate by 0
plot "{comparison_csv.as_posix()}" using 2:xtic(1) title "completion time"
"""
    gp_path.write_text(gp)
    return gp_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--max-attempts", type=int, default=30)
    ap.add_argument("--timeout", type=float, default=0.5)
    ap.add_argument("--hard-timeout", type=float, default=60.0)
    ap.add_argument("--base-port", type=int, default=16000)
    ap.add_argument("--sender", default="src/sender.py")
    ap.add_argument("--receiver", default="src/receiver.py")
    ap.add_argument("--results-dir", default="results")
    ap.add_argument("--recv-bind-wait", type=float, default=0.05)
    ap.add_argument("--cwnd-csv", default="results/cwnd.csv")
    ap.add_argument("--plot", action="store_true")
    args = ap.parse_args()

    if args.runs < 5:
        raise SystemExit("Rubric requires at least 5 runs per rate. Use --runs 5 or more.")
    if args.max_attempts < args.runs:
        raise SystemExit("--max-attempts must be >= --runs")

    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    raw_csv = results_dir / "phase5_chart1_raw.csv"
    avg_csv = results_dir / "phase5_chart1_avg.csv"
    chart1_png = results_dir / "phase5_chart1.png"
    cwnd_png = results_dir / "phase5_cwnd.png"
    comparison_png = results_dir / "phase5_phase_comparison.png"

    raw_rows: List[dict] = []
    avg_rows: List[dict] = []

    phase5_avg_0 = None

    for rate in RATES:
        ok_times: List[float] = []
        ok_count = 0
        attempt = 0

        while ok_count < args.runs and attempt < args.max_attempts:
            out_path = str(results_dir / f"tmp_phase5_rate{rate}_ok{ok_count}_att{attempt}.bmp")

            dt, status = run_one_transfer(
                rate_percent=rate,
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
                    "rate_percent": rate,
                    "run": ok_count,
                    "attempt": attempt,
                    "status": status,
                    "seconds": f"{dt:.6f}" if (status == "OK" and dt is not None) else "",
                }
            )

            if status == "OK" and dt is not None:
                ok_times.append(dt)
                ok_count += 1
            else:
                print(f"phase5 rate={rate:>2}% attempt={attempt} -> {status}", flush=True)

            attempt += 1

        if ok_times:
            avg = mean(ok_times)
            print(f"phase5 rate={rate:>2}% done ok={len(ok_times)}/{args.runs} attempts={attempt} avg={avg:.3f}s", flush=True)
        else:
            avg = None
            print(f"phase5 rate={rate:>2}% done ok=0/{args.runs} attempts={attempt} avg=NA", flush=True)

        if ok_count < args.runs:
            print(
                f"WARNING: phase5 rate={rate}% only got {ok_count}/{args.runs} OK runs after {attempt} attempts.",
                flush=True,
            )

        if rate == 0 and avg is not None:
            phase5_avg_0 = avg

        avg_rows.append(
            {
                "rate_percent": rate,
                "phase5_avg": f"{avg:.6f}" if avg is not None else "",
                "phase5_ok_runs": len(ok_times),
            }
        )

    write_csv(raw_csv, raw_rows, ["rate_percent", "run", "attempt", "status", "seconds"])
    write_csv(avg_csv, avg_rows, ["rate_percent", "phase5_avg", "phase5_ok_runs"])

    gp_chart1 = write_chart1_gnuplot(results_dir, avg_csv, chart1_png)
    gp_cwnd = write_cwnd_gnuplot(results_dir, Path(args.cwnd_csv), cwnd_png)

    comparison_csv = None
    gp_comparison = None
    if phase5_avg_0 is not None:
        comparison_csv = write_phase_comparison(results_dir, phase5_avg_0)
        gp_comparison = write_phase_comparison_gnuplot(results_dir, comparison_csv, comparison_png)

    if args.plot:
        if gnuplot_available():
            subprocess.run(["gnuplot", gp_chart1.as_posix()], check=False)

            if Path(args.cwnd_csv).exists():
                subprocess.run(["gnuplot", gp_cwnd.as_posix()], check=False)
            else:
                print(f"Missing cwnd CSV: {args.cwnd_csv}. Run sender once with --cwnd-log first.", flush=True)

            if gp_comparison is not None:
                subprocess.run(["gnuplot", gp_comparison.as_posix()], check=False)
        else:
            print("--plot requested but gnuplot not found. CSV + .gp scripts still generated.", flush=True)

    print(f"\nWrote:\n  {raw_csv}\n  {avg_csv}\n  {gp_chart1}\n  {gp_cwnd}", flush=True)

    if comparison_csv is not None:
        print(f"  {comparison_csv}\n  {gp_comparison}", flush=True)

    if chart1_png.exists():
        print(f"  {chart1_png}", flush=True)
    if cwnd_png.exists():
        print(f"  {cwnd_png}", flush=True)
    if comparison_png.exists():
        print(f"  {comparison_png}", flush=True)


if __name__ == "__main__":
    main()
